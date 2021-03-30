from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class ROLES_CHOICES(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class YamdbUser(AbstractUser):
    id = models.AutoField(primary_key=True, db_index=True)
    email = models.EmailField(verbose_name='E-Mail', unique=True)
    bio = models.TextField(verbose_name='О себе', blank=True)
    code = models.TextField(verbose_name='Код', blank=True)
    username = models.CharField(
        max_length=70,
        verbose_name='Имя пользователя',
        blank=True,
        unique=True,
    )
    role = models.CharField(
        default=ROLES_CHOICES.USER,
        max_length=100,
        choices=ROLES_CHOICES.choices,
        verbose_name='Роль пользователя'
    )
    user_permissions = None
    groups = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return any([
            self.role == ROLES_CHOICES.ADMIN,
            self.is_superuser,
            self.is_staff,
        ])

    @property
    def is_moderator(self):
        return self.role == ROLES_CHOICES.MODERATOR

    class Meta:
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class Genre(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
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

    class Meta:
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
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

    class Meta:
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Title(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        help_text='Напишите название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        blank=True,
        null=True,
        help_text='Укажите год создания',
        validators=[MinValueValidator(1900), MaxValueValidator(2021)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='категория',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанр',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True, null=True,
        help_text='Добавьте сюда описание произведения'
    )

    class Meta:
        verbose_name_plural = 'Произведения'
        ordering = ['id']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Название отзыва',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        YamdbUser,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review'
        )

    def __str__(self):
        return str(self.author)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        YamdbUser,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return str(self.author)
