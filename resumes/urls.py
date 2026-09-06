from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_resume, name="upload_resume"),
    path('api/',views.ResumeListCreateAPI.as_view(),name="resume_api")
]