from django.db import models


BSNS_POINT_Q = (
    ("201503", "201503"),
    ("201506", "201506"),
    ("201509", "201509"),
    ("201512", "201512"),
    ("201603", "201603"),
    ("201606", "201606"),
    ("201609", "201609"),
    ("201603", "201612"),
    ("201703", "201703"),
    ("201706", "201706"),
    ("201709", "201709"),
    ("201712", "201712"),
    ("201803", "201803"),
    ("201806", "201806"),
    ("201809", "201809"),
    ("201812", "201812"),
    ("201903", "201903"),
    ("201906", "201906"),
    ("201909", "201909"),
    ("201912", "201912"),
    ("202003", "202003"),
    ("202006", "202006"),
    ("202009", "202009"),
    ("202012", "202012"),
    ("202103", "202103"),
    ("202106", "202106"),
)
BSNS_POINT_Y = (
    ("2015", "2015"),
    ("2016", "2016"),
    ("2017", "2017"),
    ("2018", "2018"),
    ("2019", "2019"),
    ("2020", "2020"),
)


class CorpDataQuarter(models.Model):
    corp_name = models.CharField(max_length=20)
    time_point = models.CharField(choices=BSNS_POINT_Q, max_length=6)
    pbr = models.FloatField(null=True, blank=True)
    per = models.FloatField(null=True, blank=True)
    roe = models.FloatField(null=True, blank=True)
    debt_ratio = models.FloatField(null=True, blank=True)
    operating_margin = models.FloatField(null=True, blank=True)
    borrowing_dependence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.corp_name + self.time_point


class CorpDataYear(models.Model):
    corp_name = models.CharField(max_length=20)
    time_point = models.CharField(choices=BSNS_POINT_Y, max_length=4)
    pbr = models.FloatField(null=True, blank=True)
    per = models.FloatField(null=True, blank=True)
    roe = models.FloatField(null=True, blank=True)
    debt_ratio = models.FloatField(null=True, blank=True)
    operating_margin = models.FloatField(null=True, blank=True)
    borrowing_dependence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.corp_name + self.time_point
