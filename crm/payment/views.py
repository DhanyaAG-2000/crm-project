from django.shortcuts import render,redirect

from django.views import View

from .models import Payment,Transations

import razorpay

from decouple import config

from django.db import transaction

#  csrf exempt

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

import datetime






# Create your views here.

class StudentPaymentView(View):

    def get(self,request,*args,**kwargs):

        try:

           payment=Payment.objects.get(student__profile=request.user)

        except Payment.DoesNotExist:

            return render(request,"errorpages/error-404.html")
        
        
        transaction_obj=Transations.objects.filter(payment=payment,status="SUCCESS")

        order_id=None

        if transaction_obj.exists():

            transaction_obj=transaction_obj.first()

            order_id=transaction_obj.rzp_order_id

        data={'payment':payment,"order_id":order_id}     

        return render(request,"payments/student-payment-details.html",context=data)
        

class RazorpayView(View):

    def get(self,request,*args,**kwargs):

        with transaction.atomic():

           payment_obj=Payment.objects.get(student__profile=request.user)

           amount=payment_obj.amount
       
           client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

           data = {"amount":amount*100, "currency": "INR", "receipt": "order_rcptid_11"}

           payment = client.order.create(data=data) 

           order_id=payment.get('id')

           amount=payment.get('amount')

           Transations.objects.create(payment=payment_obj,rzp_order_id=order_id, amount=amount)

           data={'order_id':order_id,"amount":amount,"RZP_CLIENT_ID":config('RZP_CLIENT_ID')}

           return render(request,'payments/razorpay-page.html',context=data)
 

@method_decorator(csrf_exempt,name='dispatch') 

class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        data=request.POST

        rzp_order_id=data.get('razorpay_order_id')

        rzp_payment_id=data.get('razorpay_payment_id')

        rzp_signature_id=data.get('razorpay_signature')

        transaction_obj=Transations.objects.get(rzp_order_id=rzp_order_id)

        transaction_obj.rzp_payment_id= rzp_payment_id

        transaction_obj.rzp_signature_id = rzp_signature_id

        
        
        try:

            client = razorpay.Client(auth=(config('RZP_CLIENT_ID'),config('RZP_CLIENT_SECRET')))

            payment=client.utility.verify_payment_signature({
                                                'razorpay_order_id': rzp_order_id,
                                                'razorpay_payment_id': rzp_payment_id,
                                                'razorpay_signature': rzp_signature_id,
                                                })
        

            transaction_obj.status='SUCCESS'
            transaction_obj.transations_at=datetime.datetime.now()
            transaction_obj.payment.status='SUCCESS'
            transaction_obj.payment.paid_at=datetime.datetime.now()
            transaction_obj.payment.save()
            transaction_obj.save()
            
            
            return redirect('student-payment-details')
           
        
        except :

            transaction_obj.status='FAILED'

            transaction_obj.transations_at=datetime.datetime.now()

            transaction_obj.save()
        
            return redirect('student-payment-details')




       

