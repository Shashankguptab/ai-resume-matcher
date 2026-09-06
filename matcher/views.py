from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import MatchForm
from .services.matching_service import calculate_match
from   .models import MatchResult

from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from  .serializers import MatchResultSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from resumes.models import Resume
from jobs.models import JobDescription

from django.http import JsonResponse

from .services.gemini_service import analyze_resume_with_ai


@login_required
def dashboard(request):
    total_resumes = Resume.objects.filter(user=request.user).count()
    total_jobs = JobDescription.objects.filter(user=request.user).count()
    total_matches = MatchResult.objects.filter(resume__user=request.user).count()
    recent_matches = MatchResult.objects.filter(resume__user=request.user).order_by("-created_at")[:5]

    context = {
        "total_resumes": total_resumes,
        "total_jobs": total_jobs,
        "total_matches": total_matches,
        "recent_matches": recent_matches,
    }

    return render(request,"dashboard.html",context)

@login_required
def match_resume_job(request):
    result = None
    ai_result = None

    if request.method == "POST":
        form = MatchForm(request.user,request.POST)

        if form.is_valid():
            resume = form.cleaned_data["resume"]
            job = form.cleaned_data["job"]


            result = calculate_match(resume.extracted_text,job.description)
            try:
                ai_result = analyze_resume_with_ai(resume.extracted_text,job.description)

            except Exception as e:
                print("Gemini error:", e)

                ai_result = {
                    "strengths": [],
                    "missing_skills": [],
                    "suggestions": ["AI analysis is temporarily unavailable."],
                    "ats_keywords": [],
                    "candidate_summary":
                    "AI analysis could not be generated."
                }

            MatchResult.objects.create(
                resume=resume,
                job=job,
                match_score=result["match_score"],
                resume_skills=result["resume_skills"],
                job_skills=result["job_skills"],
                matched_skills=result["matched_skills"],
                missing_skills=result["missing_skills"],
            )
    else:
        form = MatchForm(request.user)

    return render(request,"match.html",
        {
            "form": form,
            "result": result,
            "ai_result":ai_result
        }
    )

@login_required
def match_history(request):
    matches=MatchResult.objects.filter(resume__user=request.user).order_by("-created_at")
    return render(request,"match_history.html",{"matches":matches})


class MatchResultListAPI(generics.ListAPIView):
    serializer_class=MatchResultSerializer
    permission_classes=[IsAuthenticated]


    def get_queryset(self):
        return MatchResult.objects.filter(user=self.request.user).order_by("-created_at")


class MatchResumeJobAPI(APIView):
    permission_classes=[IsAuthenticated]


    def post(self,request):
        resume_id=request.data.get("resume_id")
        job_id=request.data.get("job_id")

        if not resume_id or not job_id:
            return Response(
                {
                    "error":
                    "resume_id and job_id are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resume=Resume.objects.get(
                id=resume_id,
                user=request.user
            )
        except Resume.DoesNotExist:
            return Response(
                {
                    "error":
                    "Resume Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            job = JobDescription.objects.get(
                id=job_id,
                user=request.user
            )
        except JobDescription.DoesNotExist:
            return Response(
                {
                    "error":
                    "Job Description Not Found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result=calculate_match(resume.extracted_text,job.description)

        try:
            ai_result = analyze_resume_with_ai(resume.extracted_text,job.description)
        except Exception as e:
            print("Gemini error: ",e)

            ai_result={
                "strengths": [],
                "missing_skills": [],
                "suggestions": ["AI analysis is temporarily unavailable."],
                "ats_keywords": [],
                "candidate_summary":"Basic skill matching completed, but AI analysis could not be generated."
            }

        match_result=MatchResult.objects.create(
            resume=resume,
            job=job,
            match_score=result["match_score"],
            resume_skills=result["resume_skills"],
            job_skills=result["job_skills"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            ai_strengths=ai_result["strengths"],
            ai_missing_skills=ai_result["missing_skills"],
            ai_suggestions=ai_result["suggestions"],
            ats_keywords=ai_result["ats_keywords"],
            candidate_summary=ai_result["candidate_summary"],
        )

        serializer=MatchResultSerializer(
            match_result
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

