from django.db import models
from django.urls import reverse


MAX_LENGTH_NAME = 100
MAX_LENGTH_URL = 200


class MenuItem(models.Model):
    """Модель элемента меню."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=MAX_LENGTH_NAME,
        )
    url = models.CharField(
        verbose_name='URL',
        max_length=MAX_LENGTH_URL,
        blank=True,
        )
    named_url = models.CharField(
        verbose_name='Наименование URL',
        max_length=MAX_LENGTH_URL,
        blank=True
        )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Предыдущий элемент меню',
        )
    menu_name = models.CharField(
        verbose_name='Название меню',
        max_length=MAX_LENGTH_NAME,
        )

    class Meta:
        verbose_name = 'Элемент меню'
        verbose_name_plural = 'Элементы меню'

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return reverse(self.url)

    def __str__(self):
        return self.name
