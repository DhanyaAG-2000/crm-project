from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.


class LoginView(View):

    def get(self,request,*args,**kwargs):

        form=LoginForm()

        data={"form":form}

        return render(request,'authentication/login.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            user = authenticate(username=username,password=password)

            if user :

                login(request,user)

                role=user.role

                if role in ['ADMIN','SALES']:

                   return redirect('dashboard')
                
                elif  role in ['TRAINER','ACADEMIC COUNCELLOR']:

                   return redirect('students-list')
                
                elif  role in ['STUDENT']:

                   return redirect('recordings')


        error = 'u r doesnt exist'

        data = {'form':form,'error':error}

        return render(request,'authentication/login.html',context=data)
        
class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')