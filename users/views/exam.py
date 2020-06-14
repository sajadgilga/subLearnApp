from rest_framework.views import APIView
from rest_framework.response import Response
from users.utils import exam_list


class ExamView(APIView):
    def get(self, request):
        return Response(data = {"words":exam_list()})


class ExamScoreView(APIView):
    def post(self, request):
        