from django.db import models
from creator.models import Creator

CONTENT_CATEGORIES = [
    ("music", "Música"),
    ("podcast", "Podcast"),
    ("news", "Noticias"),
    ("gaming", "Gaming"),
    ("sports", "Deportes"),
    ("comedy", "Comedia"),
    ("vlog", "Vlogs / Vida Diaria"),
    ("education", "Educación"),
    ("technology", "Tecnología"),
    ("howto", "Tutoriales / How-To"),
    ("entertainment", "Entretenimiento"),
    ("fashion", "Moda / Belleza"),
    ("health", "Salud y Bienestar"),
    ("food", "Comida / Cocina"),
    ("travel", "Viajes"),
    ("documentary", "Documentales"),
    ("interview", "Entrevistas"),
    ("motivational", "Motivacional / Inspiración"),
    ("review", "Reseñas / Opiniones"),
    ("shortfilm", "Cortometrajes / Cine"),
    ("animation", "Animación"),
    ("religion", "Religión / Espiritualidad"),
    ("business", "Negocios / Emprendimiento"),
    ("finance", "Finanzas / Economía"),
    ("science", "Ciencia"),
    ("politics", "Política / Sociedad"),
    ("kids", "Contenido Infantil"),
    ("art", "Arte / Cultura"),
    ("automotive", "Automóviles / Mecánica"),
    ("realestate", "Bienes Raíces"),
    ("other", "Otro"),
]

CONTENT_CATEGORIES_DICT = dict(CONTENT_CATEGORIES)

class YoutubeCatalog(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    video_url = models.URLField()
    video_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    channel_name = models.CharField(max_length=200, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    thumbnail_url = models.URLField(blank=True)
    duration = models.CharField(max_length=20, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    
    # Personalización común
    image_cover = models.ImageField(upload_to='cover_track/', blank=True, null=True)
    creator_name = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, choices=CONTENT_CATEGORIES, blank=True)
    tags = models.CharField(max_length=250, blank=True, help_text="Palabras clave separadas por coma")
    release_year = models.PositiveIntegerField(null=True, blank=True)
    
    # Solo si aplica (música, audiovisual, etc.)
    genre = models.CharField(max_length=100, blank=True)
    subgenre = models.CharField(max_length=100, blank=True)
    album_or_series = models.CharField(max_length=150, blank=True, help_text="Nombre del álbum, serie o playlist")
    is_collaboration = models.BooleanField(default=False)
    composer = models.CharField(max_length=150, blank=True)
    producer = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.creator}"
