# Generated by Django 2.2.1 on 2019-05-09 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0008_auto_20190508_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='forks',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='repository',
            name='id',
            field=models.IntegerField(blank=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='repository',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='github.User'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='stars',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(blank=True, primary_key=True, serialize=False),
        ),
    ]
