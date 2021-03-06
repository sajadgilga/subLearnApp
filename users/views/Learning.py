from threading import Thread

from django.db.models import Q
from rest_framework import generics, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Flashcard, Profile, Subtitle, Word
from users.pagination import StandardResultsSetPagination
from users.serializers import FlashcardSerializer, SubtitleSerializer
from users.utils import get_file_from_data_url, process_sub
from users.views.authentication import error_status


class FlashCardView(generics.ListCreateAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    def get_queryset(self):
        return self.queryset.filter(learner__user=self.request.user)

    def perform_create(self, serializer):
        learner = Profile.objects.all().filter(user=self.request.user).first()
        learnt, word = self.request.data['learnt'], self.request.data['word']
        serializer.save(learner=learner,
                        learnt=learnt, word=word)


class LearnFlashCardView(generics.RetrieveUpdateAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    def get_queryset(self):
        return self.queryset.filter(learner__user=self.request.user)


class LearnView(APIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    def get(self, request, pk, learned=1, *args, **kwargs):
        try:
            _card = self.queryset.get(id=pk)
            if learned > 0:
                if _card.learnt < .2:
                    _card.learnt = .24
                _card.learnt = _card.learnt ** _card.learnt
            else:
                if _card.learnt > .9:
                    _card.learnt = .86
                _card.learnt = _card.learnt ** (_card.learnt * 10)
            _card.save()
            return Response()
        except Exception as _:
            return Response({'code': error_status['unavailable_id']}, status=status.HTTP_400_BAD_REQUEST)


class LearnSubtitle(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Subtitle.objects.all()
    serializer_class = SubtitleSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_object(self):
        return self.queryset.filter(name__contains=self.request.query_params.get('name')).first()

    def perform_create(self, serializer):
        file_url = self.request.data.get('subtitle')
        name = self.request.data.get('name')
        file, (_name, _extension) = get_file_from_data_url(file_url)
        text = file.read()
        learner = Profile.objects.filter(user=self.request.user).first()
        subtitle = Subtitle.objects.create(name=name, learner=learner, file=file)
        t = Thread(target=self.save_words, args=(text, _extension, learner, subtitle))
        t.start()

    def save_words(self, text, extension, learner, subtitle):
        result_words, result_text = process_sub(text, extension, learner.score)
        file = open(subtitle.file.path, 'w')
        file.write(result_text)
        file.close()
        subtitle.save()
        for word, trans, difficulty in result_words:
            flashcard = Flashcard.objects.filter(word__english_word=word)
            if len(flashcard) is 0:
                new_word = Word.objects.create(english_word=word, translation=trans,
                                               difficulty=difficulty)
                flashcard = Flashcard.objects.create(learner=learner, word=new_word)
            else:
                flashcard = flashcard[0]
            flashcard.subtitles.add(subtitle)
            flashcard.save()
