from django.contrib import admin
from .models import Resume

class ResumeAdmin(admin.ModelAdmin):
    list_display=[
        "id",
        "user",
        "file",
        "uploaded_at"
    ]

admin.site.register(Resume,ResumeAdmin)