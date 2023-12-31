from django import forms 
from django.core.mail import EmailMessage

class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=100)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=100)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = ' \
            送信名：{}\n \
            メールアドレス：{}\n \
            メッセージ：{}\n \
        '.format(name, email, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()

class QuizForm(forms.Form):
    answer = forms.CharField(label='答え', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['answer'].widget.attrs['class'] = 'form-control col-9'
        self.fields['answer'].widget.attrs['placeholder'] = 'ここに答えを入力してください。'
