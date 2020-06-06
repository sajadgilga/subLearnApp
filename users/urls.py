from django.urls import path

from users import views
from users.views.Learning import *
from users.views.authentication import *

app_name = "users"

urlpatterns = [
    path(r'profile/', ProfileView.as_view(), name="profile"),
    path(r'login/', UserAuthentication.as_view(), name="login"),
    path(r'logout/', logout, name="logout"),
    path(r'flashcards/', FlashCardView.as_view(), name="flashcards"),
    path(r'learn_flashcard/<pk>', LearnFlashCardView.as_view(), name="flashcards"),
    path(r'learn_subtitle/', LearnSubtitle.as_view(), name="subtitle"),
]
