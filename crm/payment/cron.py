from .models import Payment

from django.utils import timezone

import threading

from students.utility import send_email

from apscheduler.schedulers.background import BackgroundScheduler


# cron to sent reminder about payment

def remainder_email():

    current_date=timezone.now().date()

    five_days_before_date=current_date-timezone.timedelta(days=5)

    pending_payments=Payment.objects.filter(status="PENDING",student__join_date__lte=five_days_before_date)

    if pending_payments.exists():

    #    sending payment remainder to student through mail

      for payment in pending_payments:
            
            subject='payment remainder'

            recepients=[payment.student.email]

            template='email/payment-remainder.html'

            context={'name':f'{payment.student.first_name} {payment.student.last_name}'}
            
            # send_email(subject,recepients,template,context)

            thread=threading.Thread(target=send_email,args=(subject,recepients,template,context))

            thread.start()

      print("All mails send")


# apsheduler

def sheduler_start():
    
    schedule=BackgroundScheduler()

    schedule.add_job( remainder_email,'cron', hour=10,minute=0)

    schedule.start()

