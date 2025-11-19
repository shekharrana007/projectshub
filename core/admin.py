
from django.contrib import admin
from .models import StudentProfile, Project, Membership, Comment

admin.site.register(StudentProfile)
admin.site.register(Project)
admin.site.register(Membership)
admin.site.register(Comment)

# Register your models here.
