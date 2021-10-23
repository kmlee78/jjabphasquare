from django.db import models


class ChartModel(models.Model):
    name = models.CharField(max_length=20)
    corp_code = models.CharField(max_length=6)

    def __str__(self):
        return self.name
