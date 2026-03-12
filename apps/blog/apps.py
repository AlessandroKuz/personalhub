from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.blog"
    # "apps.blog" not just "blog" — because of the nested structure
