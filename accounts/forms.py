from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Code_payment

class SignUpForm(UserCreationForm):
    # email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    # referal_code = forms.CharField(max_length=6, required=False)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            # self.fields['referal_code'].help_text = "(Leave empty if you don't have)"

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        # user.referal_code = self.cleaned_data['referal_code']
        if commit:
            user.save()
        return user

class UserInformationUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', )

class PaymentForm(forms.ModelForm):
    acc_amount = forms.CharField(label="Amount", max_length=10)
    class Meta:
        model = Profile
        fields = ('phone_number','acc_amount')

    def clean_phone(self):
        phone = self.cleaned_data.get("phone_number")
        if phone == "0705860416":
            raise forms.ValidationError("Not a valid phone number")
        return phone

class GenCodeForm(forms.ModelForm):
    class Meta:
        model = Code_payment
        fields = ['amount',]

    def clean_amount(self):
        money = self.cleaned_data.get("amount")
        if money <= 499:
            raise forms.ValidationError("Amount starts from 500")
        return money

class CodePaymentForm(forms.ModelForm):
    class Meta:
        model = Code_payment
        fields = ('code',)

    def clean_code(self):
        text = self.cleaned_data["code"]
        codes = list(Code_payment.objects.all().values_list('code', flat=True))
        if text:
            if text in codes:
                present = Code_payment.objects.filter(code=text)
                for right in present:
                    if right.used == False:
                        return text
                    else:
                        raise forms.ValidationError("Code already Entered!")
            else:
                if len(text) < 6:
                    raise forms.ValidationError("Code too short!")
                elif len(text) > 6:
                    raise forms.ValidationError("Code too long!")
                else:
                    raise forms.ValidationError("Please check the code and try Again!")
        # else:
        #     raise forms.ValidationError("You must enter something please!")