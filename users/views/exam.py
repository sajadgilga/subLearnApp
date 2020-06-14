from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from users.utils import exam_list, score_by_exam
from users.models import Exam


class ExamView(APIView):
    def get(self, request):
        return Response(data = {"words":exam_list()})


class ExamScoreView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        user = request.user
        words = request.data["words"]
        answered = request.data["answered"]

        score = score_by_exam(words, answered)

        exam = Exam.objects.create(learner=user.profile, words=words, score=score)
        exam.save()

        user.profile.score = score
        user.profile.save()
