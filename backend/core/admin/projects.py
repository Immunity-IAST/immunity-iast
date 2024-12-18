"""
Отображение модели приложения.
"""

from django.contrib import admin

from core.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Отображение приложения в админке.
    """

    list_display = (
        "id",
        "user",
        "name",
        "language",
        "online",
        "created_at",
        "last_online",
    )
    list_display_links = ("name",)
    list_filter = (
        "language",
        "online",
    )
    search_fields = (
        "id",
        "name",
        "language",
        "online",
        "created_at",
        "last_online",
    )
