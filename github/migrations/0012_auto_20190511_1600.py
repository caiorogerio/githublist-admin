# Generated by Django 2.2.1 on 2019-05-11 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0011_auto_20190510_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.URLField(max_length=100),
        ),
    ]
