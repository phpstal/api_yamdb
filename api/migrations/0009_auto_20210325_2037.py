# Generated by Django 3.0.5 on 2021-03-25 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210325_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yamdbuser',
            name='username',
            field=models.CharField(blank=True, max_length=70, verbose_name='Имя пользователя'),
        ),
    ]
