from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('question-detail/<int:pk>', views.question_detail, name="question-detail"),
    path('upvote/<int:pk>', views.upvoter, name="upvote"),
    path('answer-upvote/<int:pk>/<int:pk2>', views.ansUpvoter, name="answer-upvote"),
]