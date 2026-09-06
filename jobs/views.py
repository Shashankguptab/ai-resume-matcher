from django.shortcuts import render,redirect
from  .forms import JobDescriptionForm
from django.contrib.auth.decorators import login_required
from .models import JobDescription
from .serializers import JobDescriptionSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.
@login_required
def create_job(request):
    if request.method=="POST":
        form=JobDescriptionForm(request.POST)

        if form.is_valid():
            job=form.save(commit=False)

            job.user=request.user
            job.save()

            return redirect('create_job')
    else:
        form=JobDescriptionForm()
    return render(request,'create_job.html',{'form':form})


class JobListCreateAPI(generics.ListCreateAPIView):
    serializer_class=JobDescriptionSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return JobDescription.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )