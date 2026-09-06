from rest_framework import serializers
from .models import MatchResult


class MatchResultSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title",read_only=True)
    company = serializers.CharField(source="job.company",read_only=True)
    resume_name = serializers.CharField(source="resume.file.name",read_only=True)

    class Meta:
        model = MatchResult
        fields = [
            "id",
            "resume",
            "resume_name",
            "job",
            "job_title",
            "company",
            "match_score",
            "resume_skills",
            "job_skills",
            "matched_skills",
            "missing_skills",
            "created_at",
            "ai_strengths",
            "ai_missing_skills",
            "ai_suggestions",
            "ats_keywords",
            "candidate_summary",
        ]