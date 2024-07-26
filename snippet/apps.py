from django.apps import AppConfig

class SnippetConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "snippet"
