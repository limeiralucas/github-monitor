from rest_framework import serializers

from .models import Commit, Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('name',)


class CommitSerializer(serializers.ModelSerializer):
    repository = serializers.StringRelatedField(many=False)
    avatar = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Commit
        fields = (
            'message',
            'sha',
            'author',
            'url',
            'avatar',
            'date',
            'repository',
        )
