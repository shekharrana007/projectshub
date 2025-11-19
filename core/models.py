from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.university})"


class Project(models.Model):
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('UNIV', 'University Only'),
        ('PRIVATE', 'Private'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='owned_projects', on_delete=models.CASCADE)
    university = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma separated tags")
    created_at = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')
    collaborators = models.ManyToManyField(User, through='Membership', related_name='collaborations', blank=True)
    # optional file upload
    attachment = models.FileField(upload_to='project_files/', null=True, blank=True)

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=100, default='collaborator')

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} -> {self.project.title}"


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.project.title}"

# Create your models here.
