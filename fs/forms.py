from django import forms

BSNS_YEAR = (
    (2015, "2015"),
    (2016, "2016"),
    (2017, "2017"),
    (2018, "2018"),
    (2019, "2019"),
    (2020, "2020"),
    (2021, "2021"),
)
QUARTERS = ((1, "1분기"), (2, "2분기"), (3, "3분기"), (4, "4분기"))


class FSForm(forms.Form):
    corp_name = forms.CharField(max_length=20, label="종목 이름")
    bsns_year = forms.ChoiceField(choices=BSNS_YEAR, label="공시 연도")
    quarter = forms.ChoiceField(choices=QUARTERS, label="공시 분기")
    connected = forms.BooleanField(required=False, label="연결")
