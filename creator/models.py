from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class Creator(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to="creators/", blank=True, null=True)
    activation_code = models.CharField(max_length=6, unique=True, blank=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if not self.activation_code:
            self.activation_code = self.generate_activation_code()
        super().save(*args, **kwargs)

    def generate_activation_code(self):
        return str(random.randint(100000, 999999))

    def __str__(self):
        return self.full_name or self.username


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("tiktok", "TikTok"),
        ("pinterest", "Pinterest"),
        ("telegram", "Telegram"),
        ("twitter", "X (Twitter)"),
        ("whatsapp", "WhatsApp"),
        ("amazon_music", "Amazon Music"),
        ("apple_music", "Apple Music"),
        ("deezer", "Deezer"),
        ("soundcloud", "SoundCloud"),
        ("spotify", "Spotify"),
        ("tidal", "Tidal"),
        ("twitch", "Twitch"),
        ("youtube", "YouTube"),
        ("youtube_music", "YouTube Music"),
        ("snapchat", "SnapChat"),
        ("custom", "Custom Website"),
    ]

    creator = models.ForeignKey(
        "Creator", on_delete=models.CASCADE, related_name="social_links"
    )
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.creator} - {self.platform}"
