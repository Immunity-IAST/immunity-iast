"""
Модель метки обучающего набора данных.
"""

import uuid

from django.db import models


class DatasetLabel(models.Model):
    """
    Метка для обучающего набора.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(blank=False, null=False)
    label = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Метки датасетов"
        verbose_name = "Метка датасета"

    def __str__(self):
        return str(self.id)
