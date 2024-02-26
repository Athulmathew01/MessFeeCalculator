from django.db import models
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import ExpensesSerializer
from .models import Expenses
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate, login, logout
from .form import UserCreationForm, LoginForm
from .form import ExpensesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated

class EstimateCal(generics.ListCreateAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Render the form
        form = ExpensesForm(initial={'user': request.user.id})
        return render(request, 'amount/form.html', {'form': form})
        
    # @login_required   
    def post(self, request, *args, **kwargs):
        form = ExpensesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user  
            instance.save()
            return render(request,'success_page.html') 
        else:
            return render(request, 'amount/form.html', {'form': form})



class MonthlyCal(APIView):
    def get(self,request):
        user = request.user
        queryset = Expenses.objects.filter(user=user).values().order_by("date")
        numberofdays = queryset.count()
        sumofchoices = 0 
        sumofadvance = 0 
        
        for val in queryset:
            sumofchoices += int(val['choice'])
            sumofadvance += val["deposit"]


        balance = sumofadvance - sumofchoices
        abs_balance = abs(balance)
        return render(request,"amount/list.html",{"total":sumofchoices,"balance":balance,"abs_balance":abs_balance,"values":queryset,"totaldays":numberofdays,"user":user}) 
    
def delete(request, id):
    try:
        obj =  Expenses.objects.get(pk=id)
        obj.delete()
        return render(request,'success_page.html',{'message':'Expense deleted'})
    except Exception as e:
        print(e)
        return render(request,'success_page.html',{'error':'Error deleting expense'})

def delete_all_expenses(request):
    try:
        # Filter expenses by the current user and delete them
        Expenses.objects.filter(user=request.user).delete()
        return render(request, 'success_page.html', {'message': 'All expenses deleted'})
    except Exception as e:
        print(e)
        return render(request, 'success_page.html', {'error': 'Error deleting expenses'})

# Home page
# def index(request):
#     login_form = LoginForm() 
#     return render(request, 'authenticate/index.html',{'login_form':login_form})
# # signup page
def user_signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calculate:login')
    else:
        
        form = UserCreationForm()
    return render(request,'authenticate/signup.html',{'form':form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']   
            user = authenticate(request,username = username, password = password)
            if user:
                login(request,user)
                return redirect('calculate:exp_post')
    else:
        form = LoginForm()
    return render(request, 'authenticate/index.html',{'login_form':form})

# logout page
def user_logout(request):
    request.session.delete() 
    request.session.flush()  
    logout(request)
    return redirect('calculate:login')



    

