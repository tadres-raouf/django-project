from django.db import models

# Create your models here.
class Donation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='donations')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

