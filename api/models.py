from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


#User = get_user_model()

ROLES_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator','Модератор'),
    ('admin', 'Администратор'),
]

class YamdbUser(AbstractUser):
    email = models.EmailField(verbose_name='E-Mail', unique=True)
    bio = models.TextField(verbose_name='О себе', blank=True)
    code = models.TextField(verbose_name='Код', blank=True)
    role = models.CharField(
        default='user',
        max_length=10,
        verbose_name='Роль',
        choices=ROLES_CHOICES
    )
    user_permissions = None
    groups = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


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
        null=True,
        help_text='Укажите год создания'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        db_index=False,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True, null=True,
        help_text='Добавьте сюда описание произведения'
    )
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        blank=True,
        null=True,
    )


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(YamdbUser,
                               on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(YamdbUser,
                               on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)


#class Title(models.Model):

#    name = models.CharField(max_length=140,
#                            verbose_name="Название фильма")
 #   year = models.IntegerField(
 #       validators=[MinValueValidator(1984), MaxValueValidator(2030)],
#        verbose_name="Год выпуска"
#    )
#    category = models.ForeignKey(
#        Category, on_delete=models.SET_NULL,
#        blank=True, null=True, related_name="category_title",
#        verbose_name="Категория"
#)