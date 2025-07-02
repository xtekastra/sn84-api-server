from django.db import models


# Create your models here.
class History(models.Model):
    request_id = models.CharField(max_length=50, default="")
    task_type = models.TextField(max_length=50, default="")
    image = models.TextField(default="")
    predictions = models.TextField(default='')

    version_code = models.IntegerField(default=0)
    status = models.CharField(max_length=200, default="Unknown")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.request_id)
