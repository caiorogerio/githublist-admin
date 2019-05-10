from django.db import models


def remote_values(dict):
    def wrapper(cls):
        dict.update(cls._attr_translation)
        cls._attr_translation = dict

        return cls

    return wrapper


class ImportedModel(models.Model):
    _attr_translation = {
        'id': 'id',
    }

    id = models.IntegerField(primary_key=True, blank=True)

    @classmethod
    def translate(cls, dict):
        translated_dict = {}

        for target, origin in cls._attr_translation.items():
            if origin in dict:
                translated_dict[target] = dict[origin]

        return translated_dict

    class Meta:
        abstract = True


class Language(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


@remote_values({
    'name': 'login',
    'avatar': 'avatar_url',
})
class User(ImportedModel):
    name = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(max_length=100)

    def __str__(self):
        return self.name


class RepositoryManager(models.Manager):
    def create(cls, **kwargs):
        repository = Repository.translate(kwargs)

        if kwargs['owner']:
            owner = User.translate(kwargs['owner'])
            owner, new_user = User.objects.get_or_create(**owner)
            repository['owner'] = owner

        repository['language'] = Language.objects.filter(name__iexact=kwargs['language']).first()

        cls.get_or_create(**repository)


@remote_values({
    'name': 'name',
    'description': 'description',
    'stars': 'watchers',
    'forks': 'forks',
})
class Repository(ImportedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    stars = models.IntegerField(null=True)
    forks = models.IntegerField(null=True)

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='repositories')
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='repositories')

    objects = RepositoryManager()

    def __str__(self):
        return self.name

    @property
    def owner_avatar(self):
        return self.owner.avatar
