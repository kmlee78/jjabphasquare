from django.db import models


class CorpModel(models.Model):
    corp_name = models.CharField(max_length=20)
    stock_code = models.CharField(max_length=6)
    corp_code = models.CharField(max_length=8)

    def __str__(self):
        return self.corp_name
