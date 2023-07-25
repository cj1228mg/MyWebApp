from django import forms

class SearchKeywordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " " # これにより、ラベルの「:」を消せる。また、「""」に使いたい記号があれば、代入することで「：」の代わりに変更出来る

    # required=Falseの場合、任意の入力項目になる。
    keyword = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'キーワード検索', 'class': 'class_name'}))

class FileNameForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    file_name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'ファイル名を入力'}), help_text="拡張子なしで入力してください。")

    def clean_file_name(self):
        file_name = self.cleaned_data.get('file_name')

        if ".csv" in file_name:
            raise forms.ValidationError('拡張子なしで入力してください。')
        return file_name