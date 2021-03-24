# Generated by Django 3.0.5 on 2021-03-24 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210324_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите название произведения', max_length=200, verbose_name='Заголовок')),
                ('year', models.IntegerField(blank=True, help_text='Укажите дату написания поста', null=True, verbose_name='Год создания')),
                ('description', models.TextField(blank=True, help_text='Добавьте сюда описание произведения', null=True, verbose_name='Описание произведения')),
                ('category', models.ManyToManyField(blank=True, null=True, to='api.Category')),
                ('genre', models.ManyToManyField(blank=True, null=True, to='api.Genre')),
            ],
        ),
    ]
