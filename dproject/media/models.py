from django.db import models

# Create your models here.
class ProjectImage(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='images')
    name = models.ImageField(upload_to='project_images/')
