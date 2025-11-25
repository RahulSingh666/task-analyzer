from django.db import models

# For this assignment we do not require persistent models.
# Keeping a minimal Task model in case you want to extend.
class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField(default=1.0)
    importance = models.IntegerField(default=5)
    dependencies = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
