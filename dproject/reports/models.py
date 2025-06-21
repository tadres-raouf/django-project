from django.db import models

# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reports')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True, related_name='project_reports')
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_reports')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
