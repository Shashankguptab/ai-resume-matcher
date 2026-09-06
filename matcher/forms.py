from django import forms
from resumes.models import Resume
from jobs.models import JobDescription

class MatchForm(forms.Form):
    resume=forms.ModelChoiceField(queryset=Resume.objects.all())
    job=forms.ModelChoiceField(queryset=JobDescription.objects.all())

    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['resume'].queryset=(Resume.objects.filter(user=user))
        self.fields['job'].queryset=(JobDescription.objects.filter(user=user))