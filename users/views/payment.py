from datetime import datetime, timedelta

from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Payment

import pytz

from users.serializers import PaymentSerializer

utc = pytz.UTC


class PaymentView(APIView):         #Todo: equalize datetime formats (naive or aware)
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        user: User = request.user
        amount = request.data['amount']
        days = request.data['days']

        last_time = user.end_time
        now_time = datetime.now().replace(tzinfo=utc)
        if last_time is None or last_time < now_time:
            last_time = now_time
        last_time += timedelta(days=days)

        user.end_time = last_time
        user.save()

        payment = Payment.objects.create(amount=amount, end_time=last_time, learner=user.profile)
        payment.save()

        return Response({'endtime': last_time})


class AllPaymentsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user: User = request.user
        payments = user.profile.payment_set.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
