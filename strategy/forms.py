from django import forms


FILTERS = (
    ("pbr", "PBR"),
    ("per", "PER"),
    ("roe", "ROE"),
    ("debt_ratio", "부채비율"),
    ("operating_margin", "영업이익률"),
    ("borrowing_dependence", "차입금의존도"),
)
DATA_TO_USE = (
    ("quarter", "분기별 재무데이터"),
    ("year", "연간 재무데이터"),
)


class FilterForm(forms.Form):
    filters = forms.MultipleChoiceField(
        choices=FILTERS,
        widget=forms.CheckboxSelectMultiple,
        label="사용할 필터",
        required=False,
    )
    data_to_use = forms.ChoiceField(
        choices=DATA_TO_USE,
        widget=forms.RadioSelect,
        label="사용할 데이터",
        required=True,
    )
