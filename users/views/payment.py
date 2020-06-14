from datetime import datetime, timedelta

from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Payment


class PaymentView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):        #Todo post or get?
        print(request)
        print(request.data)
        user: User = request.user
        amount = request.data['amount']
        days = request.data['days']

        last_time = user.end_time
        if last_time is None or last_time < datetime.now():
            last_time = datetime.now()
        last_time += timedelta(days=days)

        user.end_time = last_time
        user.save()

        payment = Payment.objects.create(amount=amount, end_time=last_time, learner=user.profile)
        payment.save()

        return Response({'endtime':last_time})
