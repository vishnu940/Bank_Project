"""Bankproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import User_Registration,User_login,Accountcreate,Homepage,user_logout,Transactionsview,Balancedetail,\
    Transactionhistory,index_page,about_page,contact_page,Loanpage,Creditcard,Myaccountdetail

urlpatterns = [
    path("",index_page,name="index"),
    path("register",User_Registration.as_view(),name="register"),
    path("login",User_login.as_view(),name="login"),
    path("accounts",Accountcreate.as_view(),name="create"),
    path("homepage",Homepage,name="home"),
    path("userlogout",user_logout,name="logout"),
    path("transactions",Transactionsview.as_view(),name="transfer"),
    path("balancedetail",Balancedetail.as_view(),name="balance"),
    path("transactionhistory",Transactionhistory.as_view(),name="history"),
    path("aboutus",about_page,name="about"),
    path("contactus",contact_page,name="contact"),
    path("loans",Loanpage.as_view(),name="loans"),
    path("cards",Creditcard,name="card"),
    path("accountdetails",Myaccountdetail.as_view(),name="ac_details"),
]
