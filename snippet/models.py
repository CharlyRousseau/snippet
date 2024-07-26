from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def user_directory_path(instance, filename):
    return f"user_{instance.id}/{filename}"

# CustomUser

class CustomUser(AbstractUser):

    image: models.ImageField = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True, editable=True
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

# Programming Languages choices (used in Snippet)

languages: list[tuple[str, str]] = [
    ("go", "Go"),
    ("java", "Java"),
    ("cpp", "C++"),
    ("c", "C"),
    ("rust", "Rust"),
    ("php", "Php"),
    ("ruby", "Ruby"),
    ("js", "Javascript"),
    ("ts", "Typescript"),
]

# Snippet Model
class Snippet(models.Model):
    author: models.ForeignKey[CustomUser] = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author"
    )
    title: models.CharField = models.CharField(max_length=200)
    code = models.TextField(blank=True, null=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    language: models.CharField = models.CharField(choices=languages, max_length=100, default="plaintext")
    num_like: models.PositiveIntegerField = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class LikedSnippets(models.Model):
    user: models.OneToOneField = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    snippets_liked: models.ManyToManyField = models.ManyToManyField(
        Snippet, related_name="shared_snippets", blank=True
    )

    def __str__(self) -> str:
        return self.user.username
