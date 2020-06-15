from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from users.utils import exam_list, score_by_exam
from users.models import Exam, Word


class ExamView(APIView):
    def get(self, request):
        return Response(data = {"words":exam_list()})


class ExamScoreView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    all_words = Word.objects.all()

    def post(self, request):
        user = request.user
        exam_words = request.data["words"]
        answered = request.data["answered"]

        score = score_by_exam(exam_words, answered)

        exam = Exam.objects.create(learner=user.profile, score=score)
        exam.words.set(self.all_words.filter(english_word__in=exam_words))
        exam.save()

        user.profile.score = score
        user.profile.save()

        return Response(data= {"score": score})
