from django.db import models
from accounts.models import User
from categories.models import Category
from tags.models import Tag


# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    details = models.TextField()
    tags = models.ManyToManyField(Tag, through='ProjectTag')
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_target = models.DecimalField(max_digits=12, decimal_places=2)
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField()

    is_cancelled = models.BooleanField(default=False)


class ProjectTag(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    tag = models.ForeignKey('tags.Tag', on_delete=models.CASCADE)
