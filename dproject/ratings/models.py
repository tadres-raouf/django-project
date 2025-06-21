from django.db import models

# Create your models here.
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='ratings')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField()  # 1 to 5
