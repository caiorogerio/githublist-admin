from django.db.models import Prefetch
from rest_framework import serializers, generics

from .models import Language, Repository, User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'avatar',)


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Repository
        fields = ('name', 'description', 'owner', 'forks', 'stars', 'link', 'git',)


class LanguageDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='github:language-detail', read_only=True, lookup_field='slug')
    repositories = RepositorySerializer(many=True, read_only=True)

    class Meta:
        model = Language
        fields = ('url', 'name', 'repositories',)


class LanguageListSerializer(LanguageDetailSerializer):

    class Meta:
        model = Language
        fields = ('url', 'name', 'repositories_number',)


class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.get_queryset()
    serializer_class = LanguageListSerializer
    lookup_field = 'slug'
    paginate_by = 50
    ordering = ('name',)


class LanguageDetailView(generics.RetrieveAPIView):
    queryset = Language.objects.prefetch_related(
        Prefetch(
            'repositories',
            queryset=Repository.objects.order_by('-stars')
        )
    )
    serializer_class = LanguageDetailSerializer
    lookup_field = 'slug'
