from django.db import models
from resumes.models import Resume
from jobs.models import JobDescription

# Create your models here.
class MatchResult(models.Model):
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE)
    job = models.ForeignKey(JobDescription,on_delete=models.CASCADE)
    match_score = models.FloatField()
    resume_skills = models.JSONField(default=list)
    job_skills = models.JSONField(default=list)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.resume} - "
            f"{self.job.title} - "
            f"{self.match_score}%"
        )

    ai_strengths = models.JSONField(default=list,blank=True)
    ai_missing_skills = models.JSONField(default=list,blank=True)
    ai_suggestions = models.JSONField(default=list,blank=True)
    ats_keywords = models.JSONField(default=list,blank=True)
    candidate_summary = models.TextField(blank=True)