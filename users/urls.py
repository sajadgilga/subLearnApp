from django.urls import path

from users import views
from users.views.Learning import *
from users.views.authentication import *
from users.views.exam import *
from users.views.payment import *

app_name = "users"

urlpatterns = [
    path(r'profile/', ProfileView.as_view(), name="profile"),
    path(r'login/', UserAuthentication.as_view(), name="login"),
    path(r'logout/', logout, name="logout"),
    path(r'flashcards/', FlashCardView.as_view(), name="flashcards"),
    path(r'learn_flashcard/<pk>', LearnFlashCardView.as_view(), name="flashcards"),
    path(r'learn_subtitle/', LearnSubtitle.as_view(), name="subtitle"),
    path(r'learn/<int:pk>/', LearnView.as_view(), name="flashcards"),
    path(r'learn/<int:pk>/<int:learned>/', LearnView.as_view(), name="flashcards"),
    path('exam/', ExamView.as_view(), name="exam"),
    path('exam/score/', ExamScoreView.as_view(), name="exam_score"),
    path(r'payment/', PaymentView.as_view(), name='payment')
]
