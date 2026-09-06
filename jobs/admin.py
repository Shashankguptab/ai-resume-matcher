from django.contrib import admin
from  .models import JobDescription
# Register your models here.

class JobDescriptionAdmin(admin.ModelAdmin):
    list_display=[
        "id",
        "title",
        "company",
        "user",
        "created_at",
    ]

admin.site.register(JobDescription,JobDescriptionAdmin)