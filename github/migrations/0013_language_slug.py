# Generated by Django 2.2.1 on 2019-05-13 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0012_auto_20190511_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='slug',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
