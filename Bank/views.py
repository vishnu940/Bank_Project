from django.shortcuts import render,redirect
from .forms import Registerform,Loginform,Accountsform,Transactioncreateform,Loanform
from  .models import CustomUser,Accounts,Transactions,Loans
from django.contrib.auth import authenticate,login as djangologin,logout
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from .decorators import account_validator
# Create your views here.

class User_Registration(TemplateView):
    model=CustomUser
    template_name = "Bank/register.html"
    context={}
    form_class=Registerform
    def get(self, request, *args, **kwargs):
        self.context["form"]=self.form_class()
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            self.context["form"]=form
            return render(request,self.template_name,self.context)

class User_login(TemplateView):
    model=CustomUser
    template_name = "Bank/login.html"
    context={}
    form_class=Loginform
    def get(self, request, *args, **kwargs):
        self.context["form"]=self.form_class()
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=self.model.objects.get(username=username)

            if(user.username==username) & (user.password==password):
                djangologin(request,user)
                return redirect("home")
            else:
                self.context["form"]=form
                return render(request, self.template_name, self.context)


@method_decorator(account_validator,name="dispatch")
class Accountcreate(TemplateView):
    model=Accounts
    template_name = "Bank/accountcreate.html"
    context={}
    form_class=Accountsform
    def get(self, request, *args, **kwargs):
        account_number = ""
        account=self.model.objects.all().last()
        if account:
            accno=int(account.account_number.split("-")[1])+1
            account_number="sbk-"+str(accno)
        else:
            account_number="sbk-1000"
        self.context["form"]=self.form_class(initial={"account_number":account_number,"user":request.user})
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            self.context["form"]=form
            return render(request, self.template_name, self.context)


def Homepage(request):
    context={}
    try:
        account = Accounts.objects.get(user=request.user)
        status = account.active_status
        flag = True if status == "active" else False
        context["flag"] = flag
        return render(request,"Bank/home.html",context)
    except:
        return render(request, "Bank/home.html",context)

def user_logout(request):
    logout(request)
    return redirect("login")

class Getusermixin(object):
    def get_user(self,account_num):
        return Accounts.objects.get(account_number=account_num)


class Transactionsview(TemplateView,Getusermixin):
    model=Transactions
    template_name = "Bank/transactions.html"
    form_class =Transactioncreateform
    context={}
    
    def get(self, request, *args, **kwargs):
        self.context["form"]=self.form_class(initial={"user":request.user})
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            to_account=form.cleaned_data.get("to_account")
            amount=form.cleaned_data.get("amount")
            remarks=form.cleaned_data.get("remarks")
            account=self.get_user(to_account)
            account.balance+=int(amount)
            account.save()
            crr_account=Accounts.objects.get(user=request.user)
            crr_account.balance-=int(amount)
            crr_account.save()
            transaction=Transactions(user=request.user,amount=amount,to_accno=to_account,remarks=remarks)
            transaction.save()
            return redirect("home")
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)


class Balancedetail(TemplateView):
    model=Accounts
    template_name = "Bank/balance.html"
    context = {}

    def get(self, request, *args, **kwargs):
        account=self.model.objects.get(user=request.user)
        self.context["balance"]=account
        return render(request,self.template_name,self.context)

class Transactionhistory(TemplateView):
    template_name = "Bank/transactionhistory.html"
    def get(self, request, *args, **kwargs):
        debit_transaction=Transactions.objects.filter(user=request.user)
        l_user=Accounts.objects.get(user=request.user)
        credit_transaction=Transactions.objects.filter(to_accno=l_user.account_number)
        return render(request,self.template_name,{"debit":debit_transaction,"credit":credit_transaction})


def index_page(request):
    return render(request,"Bank/homeindex.html")

def about_page(request):
    return render(request,"Bank/about.html")

def contact_page(request):
    return render(request,"Bank/contact.html")

class Loanpage(TemplateView):
    model=Loans
    template_name = "Bank/loans.html"
    form_class =Loanform
    context={}
    def get(self, request, *args, **kwargs):
        self.context["form"]=self.form_class()
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")

        return render(request,self.template_name,self.context)

def Creditcard(request):
    form=Loanform()
    context={}
    context["form"]=form
    form=Loanform(request.POST)
    if form.is_valid():
        form.save()
        return redirect("index")

    return render(request,"Bank/cards.html",context)

class Myaccountdetail(TemplateView):
    model=Accounts
    template_name="Bank/accountdetail.html"
    context={}
    def get(self, request, *args, **kwargs):
        account=self.model.objects.get(user=request.user)
        self.context["account"]=account
        return render(request,self.template_name,self.context)
