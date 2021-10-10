from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.core.paginator import Page, Paginator
# Create your views here.
def home(request):
    return render(request,'home.html')

def transaction_list(request,page_num):
    """
    Used to get transaction list
    """
    transactions = Transaction.objects.all().order_by("-id")
    p = Paginator(transactions,15)
    page_count = p.count//15
    if p.count%15!=0:
        page_count+=1
    if page_num==0:
        return(request, 'transaction_history.html',{'transaction':0,'page_count':0,'next':page_num+1,'page_num':page_num,'previous':page_num-1})
    try:
        transactions = p.page(page_num)
    except:
        transactions = p.page(1)
        page_num = 1
    return render(request,'transaction_history.html',{'transactions':transactions,'page_count':page_count,'next':page_num+1,'page_num':page_num,'previous':page_num-1})

def customer_list(request):
    customers = User.objects.all()
    for c in customers:
        c.account_no = 'xxxxxxxxxxx'+str(c.account_no)[-4:]
    return render(request,'customers.html',{'customers':customers})

def transfer_amount(request):
    """
    Used to transfer amount between users
    """
    if request.method=='GET':
        customers = User.objects.all()
        ifsc_codes = []
        for c in customers:
            if c.ifsc_code not in ifsc_codes:   ifsc_codes.append(c.ifsc_code)
        return render(request,'transfer_money.html',{'customers':customers,'ifsc_codes':ifsc_codes})
    else:
        data = request.POST
        sender = data.get('sender')
        receiver = data.get('receiver')
        amount = data.get('amount')
        try:
            amount = float(data.get('amount'))
            sender_ifsc_code = data.get('sender_ifsc_code')
            receiver_ifsc_code = data.get('receiver_ifsc_code')
        except:
            messages.info(request,"All fields are required.")
            return redirect('transfer_money')
            

        sender = User.objects.get(id=int(sender))
        receiver = User.objects.get(id=int(receiver))
        sender_ifsc = sender.ifsc_code
        receiver_ifsc = receiver.ifsc_code

        if sender==receiver:
            messages.info(request,'Transaction can not possible between same users.')
            return redirect('transfer_money')
        elif amount<=0:
            messages.info(request,'Amount can not be zero or negative.')
            return redirect('transfer_money')
        elif (sender_ifsc_code!=sender_ifsc) or (receiver_ifsc_code!=receiver_ifsc):
            messages.info(request,"Incorrect IFSC number.")
            return redirect('transfer_money')
        elif amount>sender.balance:
            messages.info(request,"Sender's account balance is less than amount")
            return redirect('transfer_money')
        else:
            sender.balance = float(sender.balance)-amount
            receiver.balance = float(receiver.balance)+amount
            sender.save()
            receiver.save()
            Transaction.objects.create(sender=sender,receiver=receiver,balance=amount)
            return HttpResponseRedirect(reverse('transaction_history',args=[1]))

def customer_detail(request,id):
    """
    Used to get customer detail
    """
    if request.method=='GET':
        customer = User.objects.get(id=id)
        customers = User.objects.all()
        ifsc_codes = []
        for c in customers:
            if c.ifsc_code not in ifsc_codes:   ifsc_codes.append(c.ifsc_code)
        return render(request,'customer_detail.html',{'customer':customer,'customers':customers,'ifsc_codes':ifsc_codes})
    else:
        data = request.POST
        sender = data.get('sender')
        receiver = data.get('receiver')
        try:
            amount = float(data.get('amount'))
            receiver_ifsc_code = data.get('receiver_ifsc_code')
        except:
            messages.info(request,"All fields are required.")
            return HttpResponseRedirect(reverse('customer_detail',args=[id]))

        sender = User.objects.get(id=int(sender))
        receiver = User.objects.get(id=int(receiver))
        ifsc_code = receiver.ifsc_code

        if amount<=0:
            messages.info(request,'Amount can not be zero or negative.')
            return HttpResponseRedirect(reverse('customer_detail',args=[id]))
        elif amount>sender.balance:
            messages.info(request,"Sender's account balance is less than amount.")
            return HttpResponseRedirect(reverse('customer_detail',args=[id]))
        elif ifsc_code!=receiver_ifsc_code:
            messages.info(request,"Incorrect IFSC number.")
            return HttpResponseRedirect(reverse('customer_detail',args=[id]))
        else:
            sender.balance = float(sender.balance)-amount
            receiver.balance = float(receiver.balance)+amount
            sender.save()
            receiver.save()
            Transaction.objects.create(sender=sender,receiver=receiver,balance=amount)
            return HttpResponseRedirect(reverse('transaction_history',args=[1]))


def about(request):
    """
    Used to get about system
    """
    return render(request,'about.html')

def terms_conditions(request):
    """
    Terms & Conditions
    """
    return render(request,'terms_conditions.html')
