from rest_framework import serializers, generics

from .models import Language, Repository, User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('name', )


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Repository
        fields = ('name', 'description', 'owner', 'forks', 'stars',)


class LanguageDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='github:language-detail', read_only=True)
    repositories = RepositorySerializer(many=True, read_only=True)

    class Meta:
        model = Language
        fields = ('url', 'name', 'repositories',)


class LanguageListSerializer(LanguageDetailSerializer):

    class Meta:
        model = Language
        fields = ('url', 'name',)


class LanguageView(generics.ListAPIView):
    queryset = Language.objects.all()
