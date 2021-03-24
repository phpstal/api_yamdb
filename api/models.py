from django.contrib.auth import get_user_model
from django.db import models


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank=True, null=True,
        help_text='Напишите название жанра'
    )

    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text=('Укажите адрес для нового жанра. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )


class Category(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank=True, null=True,
        help_text='Напишите название категории'
    )

    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text=('Укажите адрес для новой категории. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        help_text='Напишите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        blank=True, 
        help_text='Укажите дату написания поста'
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True, null=True,
        help_text='Добавьте сюда описание произведения'
    )
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ManyToManyField(Category, blank=True)
