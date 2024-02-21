from django.urls import path

from scores.views import ManageScoreView

urlpatterns = [
    path('', ManageScoreView.as_view()),

]