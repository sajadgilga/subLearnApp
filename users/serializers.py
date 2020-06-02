from rest_framework import serializers

from users.models import User, Profile, Word


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'name', 'image', 'enabled',)
        read_only_fields = ('username', 'enabled',)

    def get_image(self, obj):
        if not obj.image:
            return ''
        return obj.image.storage.base_location + '/' + obj.image.name

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name


class LearnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'score',)

    def update(self, instance, validated_data):
        user_serializer = self.fields['user']
        user_instance = instance.user
        user_data = validated_data.pop('user')
        user = user_serializer.update(instance=user_instance, validated_data=user_data)
        profile_updated = super().update(instance, validated_data)
        profile_updated.user = user
        return instance


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('__ALL__')
