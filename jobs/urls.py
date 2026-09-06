from django.urls import path
from . import views


urlpatterns = [
    path("create/",views.create_job,name="create_job"),
    path('api/',views.JobListCreateAPI.as_view(),name='job_api')
]