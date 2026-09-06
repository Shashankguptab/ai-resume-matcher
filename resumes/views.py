from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from  .forms import ResumeUploadForm
from  .services.resume_parser import extract_text_from_pdf
from .serializers import ResumeSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Resume
# Create your views here.

@login_required
def upload_resume(request):
    extracted_text=None
    if request.method=="POST":
        form=ResumeUploadForm(request.POST,request.FILES)

        if form.is_valid():
            resume=form.save(commit=False)
            resume.user = request.user
            resume.save()

            extracted_text=extract_text_from_pdf(resume.file.path)
            resume.extracted_text=extracted_text
            resume.save()


            # return redirect("upload_resume")
    else:
        form=ResumeUploadForm()
    return render(request, "upload_resume.html", 
    {
        "form": form,
        "extracted_text": extracted_text
    })

class ResumeListCreateAPI(generics.ListCreateAPIView):
    serializer_class=ResumeSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):         #prevents one user from seeing another user's name
        return Resume.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        resume=serializer.save(user=self.request.user)
        extracted_text=extract_text_from_pdf(resume.file.path)
        resume.extracted_text=extracted_text
        resume.save()

        