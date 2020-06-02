from django.contrib.auth import authenticate, login
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Profile, User, Flashcard
from users.serializers import LearnerSerializer, FlashCardSerializer

error_status = {
    'auth_fields_defect': 101,
    'wrong_credentials': 102,
}


class UserAuthentication(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **vargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        user = self.queryset.filter(username=username)
        if len(user) is 0:
            user = User.objects.create(username=username)
            user.set_password(raw_password=password)
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            user.save()
            Profile(user=user, score=0).save()
        else:
            user = authenticate(request, username=username, password=password)
            if not user:
                return Response({'code': error_status['wrong_credentials']}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


@api_view(['GET', ])
def logout(request):
    logout(request)
    return Response()


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = LearnerSerializer

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class FlashCardView(generics.ListCreateAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashCardSerializer

    def get_queryset(self):
        return self.queryset.filter(learner__user=self.request.user)

    def perform_create(self, serializer):
        learner = Profile.objects.all().filter(user=self.request.user).first()
        learnt, word = self.request.data['learnt'], self.request.data['word']
        serializer.save(learner=learner,
                        learnt=learnt, word=word)


class LearnFlashCardView(generics.RetrieveUpdateAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashCardSerializer

    def get_queryset(self):
        return self.queryset.filter(learner__user=self.request.user)
