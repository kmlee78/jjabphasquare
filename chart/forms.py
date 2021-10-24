from django import forms

CHOICES = (("10", "10일"), ("20", "20일"), ("60", "60일"))
PERIODS = tuple((str(i), str(i)) for i in range(1, 366))


class ChartForm(forms.Form):
    corp_name = forms.CharField(max_length=20, label="종목 이름")
    period = forms.ChoiceField(choices=PERIODS, label="검색 기간")
    moving_average = forms.MultipleChoiceField(
        choices=CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="이동평균선",
        required=False,
    )
