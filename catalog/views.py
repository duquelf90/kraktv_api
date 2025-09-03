from django.conf import settings
from googleapiclient.discovery import build
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from catalog.models import CONTENT_CATEGORIES, CONTENT_CATEGORIES_DICT, YoutubeCatalog
from catalog.utils import convert_iso_duration


class YouTubeChannelInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, channel_id):
        api_key = settings.YOUTUBE_API_KEY
        youtube = build("youtube", "v3", developerKey=api_key)

        try:
            channel_request = youtube.channels().list(
                part="statistics,contentDetails", id=channel_id
            )
            channel_response = channel_request.execute()

            channel_stats = channel_response["items"][0]["statistics"]
            total_videos = channel_stats.get("videoCount", 0)
            subscriber_count = channel_stats.get("subscriberCount", 0)
            view_count = channel_stats.get("viewCount", 0)

            uploads_playlist_id = channel_response["items"][0]["contentDetails"][
                "relatedPlaylists"
            ]["uploads"]

            videos_request = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=10,  
            )
            videos_response = videos_request.execute()

            video_details = []
            total_comments = 0
            for item in videos_response["items"]:
                video_id = item["snippet"]["resourceId"]["videoId"]

                video_request = youtube.videos().list(
                    part="snippet,contentDetails,statistics", id=video_id
                )
                video_response = video_request.execute()

                category_id = video_response["items"][0]["snippet"]["categoryId"]
                category_request = youtube.videoCategories().list(
                    part="snippet", id=category_id
                )
                category_response = category_request.execute()
                category_label = (
                    category_response["items"][0]["snippet"]["title"]
                    if category_response["items"]
                    else "Unknown"
                )
                iso_duration = video_response["items"][0]["contentDetails"].get(
                    "duration", ""
                )
                readable_duration = convert_iso_duration(iso_duration)
                mapped_category = CONTENT_CATEGORIES_DICT.get(
                    category_label.lower(), "other"
                )
                mapped_category_key = next(
                    (
                        key
                        for key, value in CONTENT_CATEGORIES
                        if value == mapped_category
                    ),
                    "other",
                )

                video_info = {
                    "video_id": video_response["items"][0]["id"],
                    "channel_name": video_response["items"][0]["snippet"][
                        "channelTitle"
                    ],
                    "title": video_response["items"][0]["snippet"]["title"],
                    "description": video_response["items"][0]["snippet"]["description"],
                    "published_at": video_response["items"][0]["snippet"][
                        "publishedAt"
                    ],
                    "thumbnail_url": video_response["items"][0]["snippet"][
                        "thumbnails"
                    ]["maxres"]["url"],
                    "view_count": video_response["items"][0]["statistics"].get(
                        "viewCount", 0
                    ),
                    "like_count": video_response["items"][0]["statistics"].get(
                        "likeCount", 0
                    ),
                    "comment_count": video_response["items"][0]["statistics"].get(
                        "commentCount", 0
                    ),
                    "tags": video_response["items"][0]["snippet"]["tags"],
                    "duration": readable_duration,
                    "category": category_label,
                }

                total_comments += int(video_info["comment_count"])
                video_details.append(video_info)

                if not YoutubeCatalog.objects.filter(
                    video_id=video_info["video_id"]
                ).exists():
                    tags_string = ", ".join(video_info["tags"])

                    try:
                        YoutubeCatalog.objects.create(
                            creator=request.user,
                            video_url=f"https://www.youtube.com/watch?v={video_info['video_id']}",
                            video_id=video_info["video_id"],
                            title=video_info["title"],
                            channel_name=video_info["channel_name"],
                            published_at=video_info["published_at"],
                            thumbnail_url=video_info["thumbnail_url"],
                            view_count=video_info["view_count"],
                            tags=tags_string,
                            image_cover=video_info["thumbnail_url"],
                            duration=video_info["duration"],
                            category=mapped_category_key,
                        )
                    except Exception as e:
                        print(f"Error al guardar el objeto: {e}")

            response_data = {
                "channel_id": channel_id,
                "total_videos": total_videos,
                "subscriber_count": subscriber_count,
                "view_count": view_count,
                "total_comments": total_comments,
                "videos": video_details,
            }

            return JsonResponse(
                {"message": "Videos sincronizados", "data": response_data}, status=201
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
