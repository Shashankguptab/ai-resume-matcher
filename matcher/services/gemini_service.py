from google import genai
from django.conf import settings
from pydantic import BaseModel, Field


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

class ResumeAnalysis(BaseModel):
    strengths:list[str]=Field(
        description="Important strengths from the resume that match the job"
    )

    missing_skills: list[str] = Field(
        description="Important job skills that are missing from the resume."
    )

    suggestions: list[str] = Field(
        description="Practical suggestions to improve the resume for this job."
    )

    ats_keywords: list[str] = Field(
        description="Important ATS keywords from the job description."
    )

    candidate_summary: str = Field(
        description="Short summary of how suitable the candidate is for the role."
    )

def analyze_resume_with_ai(resume_text,job_text):

    prompt=f"""
You are an AI Analyzer.

Compare the Candidate's resume with the job descripion.

Only use information actually present in the resume and job description.

Identify:
- candidate strengths relevant to the job
- important missing skills
- resume improvement suggestions
- useful ATS keywords from the job description
- a short candidate suitability summary

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,

        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ResumeAnalysis.model_json_schema(),
        },
    )

    analysis = ResumeAnalysis.model_validate_json(
        interaction.output_text
    )

    return analysis.model_dump()
