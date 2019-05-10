from django.dispatch import receiver
from django.db.models import Count
from django.db.models.signals import post_save, post_delete

from .models import Language, Repository, User
from .services import get_repositories


@receiver(post_save, sender=Language)
def get_github_data(sender, instance, created, **kwargs):
    if not created:
        Repository.objects.filter(language=instance).delete()
        delete_orphans_users()

    repos = get_repositories(instance.name)
    for repo in repos:
        Repository.objects.create(**repo)


@receiver(post_delete, sender=Language)
def delete_orphans_users(**kwargs):
    User.objects\
        .annotate(Count('repositories'))\
        .filter(repositories__count=0)\
        .delete()
