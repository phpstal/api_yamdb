# Generated by Django 3.0.5 on 2021-03-26 08:43

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Напишите название категории', max_length=200, null=True, verbose_name='Заголовок')),
                ('slug', models.SlugField(help_text='Укажите адрес для новой категории. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='Слаг')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Напишите название жанра', max_length=200, null=True, verbose_name='Заголовок')),
                ('slug', models.SlugField(help_text='Укажите адрес для нового жанра. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='Слаг')),
            ],
        ),
        migrations.CreateModel(
            name='YamdbUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-Mail')),
                ('bio', models.TextField(blank=True, verbose_name='О себе')),
                ('code', models.TextField(blank=True, verbose_name='Код')),
                ('role', models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', max_length=10, verbose_name='Роль')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите название произведения', max_length=200, verbose_name='Заголовок')),
                ('year', models.IntegerField(blank=True, help_text='Укажите год создания', null=True, verbose_name='Год создания')),
                ('description', models.TextField(blank=True, help_text='Добавьте сюда описание произведения', null=True, verbose_name='Описание произведения')),
                ('rating', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('category', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='api.Category')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', to='api.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий оценки')),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.YamdbUser', verbose_name='Автор')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.Title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Отзыв с оценкой',
                'ordering': ['-pub_date'],
                'unique_together': {('title', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.YamdbUser', verbose_name='Автор')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Review', verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Комментарий к оценке',
                'ordering': ['-pub_date'],
            },
        ),
    ]
