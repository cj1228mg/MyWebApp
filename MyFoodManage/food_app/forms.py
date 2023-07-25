# import sys
# print(sys.executable)
# exit()

from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput

class SearchForm(forms.Form):
    search = forms.CharField(label="検索", required=False)

class CategoryChoices(models.TextChoices):
    NO_CHOICES = "", "未選択"
    # CANNED_FOOD = "缶詰・瓶詰", "缶詰・瓶詰"
    # TOHU_NATTO_TUKEMONO = "豆腐・納豆・漬物", "豆腐・納豆・漬物"
    # SEASONING = "調味料", "調味料"
    # FROZEN = "冷凍", "冷凍"
    # SNACKS = "お菓子", "お菓子"
    MEAT = "豚肉", "豚肉"


class AddFoodForm(forms.Form):
    
    name = forms.CharField(label="食材名")
    category = forms.ChoiceField(choices=CategoryChoices.choices, label="カテゴリー")
    expiry_date = forms.DateField(label="賞味期限", required=False, widget=DatePickerInput(format="%Y-%m-%d"))
    expiration_date = forms.DateField(label="消費期限", required=False, widget=DatePickerInput(format="%Y-%m-%d"))

    # ToDo: commentをmemoに変更する
    memo = forms.CharField(label="メモ", required=False, widget=forms.Textarea())

    def clean_category(self):
        category = self.cleaned_data['category']

        if category == "":
            raise ValidationError("カテゴリーを選択してください。")

        return category
