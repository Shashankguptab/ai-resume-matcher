from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard"),
    path("match/",views.match_resume_job,name="match_resume_job"),
    path("history/",views.match_history,name="match_history"),
    path('api/results/',views.MatchResultListAPI.as_view(),name="match_results_api"),
    path('api/match/',views.MatchResumeJobAPI.as_view(),name="match_api"),
]