from django import forms
from .models import CustomUser,Accounts,Transactions,Loans
from django.forms import ModelForm


class Registerform(ModelForm):
    class Meta:
        model=CustomUser
        fields=["username","password","email","phone","age"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control","placeholder":"username"}),
            "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}),
            "email":forms.TextInput(attrs={"class":"form-control","placeholder":"Email"}),
            "phone":forms.NumberInput(attrs={"class":"form-control","placeholder":"Phone"}),
            "age":forms.NumberInput(attrs={"class":"form-control","placeholder":"Age"})
        }

class Loginform(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))

class Accountsform(ModelForm):
    class Meta:
        model=Accounts
        fields="__all__"
        widgets={
            "account_number":forms.TextInput(attrs={'readonly':'readonly'}),

        }

class Transactioncreateform(forms.Form):
    user=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","readonly":"readonly"}))
    to_account=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    confirm_account=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    amount=forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control"}))
    remarks=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        to_account=cleaned_data.get("to_account")
        confirm_account=cleaned_data.get("confirm_account")
        amount=int(cleaned_data.get("amount"))
        user=cleaned_data.get("user")


        try:
            account=Accounts.objects.get(account_number=to_account)

        except:
            msg = "Invalid Account Number"
            self.add_error("to_account", msg)

        if to_account != confirm_account:
            msg="Account number mismatch"
            self.add_error("to_account",msg)

        account=Accounts.objects.get(user__username=user)
        aval_balance=account.balance
        if amount>aval_balance:
            msg="Insufficient balance"
            self.add_error("amount",msg)


class Loanform(ModelForm):
    class Meta:
        model=Loans
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"Name"}),
            "email":forms.TextInput(attrs={"class":"form-control","placeholder":"Email"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Address"}),
            "phone":forms.NumberInput(attrs={"class":"form-control","placeholder":"Phone"})
        }






