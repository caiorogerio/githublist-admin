# Generated by Django 2.2.1 on 2019-05-10 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0010_auto_20190509_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='repository',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='github.User'),
        ),
    ]
