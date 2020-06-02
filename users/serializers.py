from rest_framework import serializers

from users.models import User, Profile, Word, Flashcard


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
        if validated_data.get('user'):
            user_serializer = self.fields['user']
            user_instance = instance.user
            user_data = validated_data.pop('user')
            user = user_serializer.update(instance=user_instance, validated_data=user_data)
            profile_updated = super().update(instance, validated_data)
            profile_updated.user = user
        else:
            profile_updated = super().update(instance, validated_data)
        return instance


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class FlashCardSerializer(serializers.ModelSerializer):
    word = WordSerializer()

    class Meta:
        model = Flashcard
        fields = ('learnt', 'word', 'id')

    def update(self, instance, validated_data):
        if validated_data.get('word'):
            word_serializer = self.fields['word']
            word_instance = instance.word
            word_data = validated_data.pop('word')
            word = word_serializer.update(instance=word_instance, validated_data=word_data)
            card_updated = super().update(instance, validated_data)
            card_updated.word = word
        else:
            card_updated = super().update(instance, validated_data)
        return instance

    def create(self, validated_data):
        word_data = validated_data.pop('word')
        word = Word.objects.create(**word_data)
        instance = Flashcard.objects.create(**validated_data, word=word)
        return instance
