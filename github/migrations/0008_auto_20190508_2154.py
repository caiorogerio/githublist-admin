# Generated by Django 2.2.1 on 2019-05-08 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0007_auto_20190508_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='forks',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repository',
            name='stars',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
