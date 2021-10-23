from django.db import models


class ChartModel(models.Model):
    corp_name = models.CharField(max_length=20)
    stock_code = models.CharField(max_length=6)

    def __str__(self):
        return self.name
