from django.urls import path
from .views import (
    SocialLinkListCreateView,
    SocialLinkDetailView,
    SocialLinkBulkUpdateView,
    CreatorDetailView,
)

urlpatterns = [
    path("me/", CreatorDetailView.as_view(), name="creator-detail"),
    path("social-links/",SocialLinkListCreateView.as_view(),name="social-link-list-create"),
    path("social-links/<int:pk>/",SocialLinkDetailView.as_view(),name="social-link-detail"),
    path("social-links/bulk-update/",SocialLinkBulkUpdateView.as_view(),name="social-link-bulk-update"),
]
