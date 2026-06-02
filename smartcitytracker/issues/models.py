from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    CATEGORY = [
        ('pothole', 'Pothole'),
        ('garbage', 'Garbage'),
        ('streetlight', 'Streetlight'),
        ('water', 'Water Leakage'),
        ('other', 'Other'),
    ]
    STATUS = [
        ('reported', 'Reported'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    SEVERITY = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]
    severity = models.CharField(max_length=20, choices=SEVERITY, default="medium")

    upvotes = models.ManyToManyField(User, related_name="upvoted_issues", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY)
    photo = models.ImageField(upload_to='issue_photos/', blank=True, null=True)
    video = models.FileField(upload_to='issue_videos/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_upvotes(self):
        return self.upvotes.count()
    def __str__(self):
        return f"{self.title} ({self.status})"

# In-app notification (no email)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



