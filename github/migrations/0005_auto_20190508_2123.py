# Generated by Django 2.2.1 on 2019-05-08 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0004_auto_20190508_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.TextField(max_length=300),
        ),
    ]
