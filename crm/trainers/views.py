
from django.shortcuts import render,redirect,get_object_or_404

from django.http import HttpResponse

from django.views.generic import View

from .models import DistrictChoices

from .utility import get_employee_number,get_password

from .models import Trainers

from .forms import TrainerRegisterForm

from django.db.models import Q

from authentication.models import Profile

from django.db import transaction

from django.contrib.auth.decorators import login_required

from django.utils.decorators import  method_decorator

from authentication.permission import permission_roles


# Create your views here.



class GetTrainerObject:

    # def get_student(self,pk):

    def get_trainer(self,request,uuid):

        try :

            Trainer = Trainers.objects.get(uuid=uuid)

            return Trainer
        
        except :

            return render(request,"errorpages/error-404.html")
        

# @method_decorator(login_required,name='dispatch')

# @method_decorator(permission_roles(roles=["ADMIN","SALES"]),name='dispatch')

class DashBoardView(View) :

    def get(self,request,*args,**kwargs):

        return render(request,'trainers/dashboard.html')
    #  roles-----sales,admin
# @method_decorator(permission_roles(roles=["ADMIN","SALES","Trainer","ACADEMIC_COUNCELLOR"]),name='dispatch')

class TrainersListView(View) :

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        role=request.user.role

        if role in ['TRAINER']:

            trainer=Trainers.objects.filter(active_status = True,trainer__profile=request.user)

            
            if query:

              trainer=Trainers.objects.filter(Q(active_status=True)&Q(trainer__profile=request.user)&(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(course__name__icontains=query)))
        
        elif role in ['ACADEMIC COUNCELLOR']: 

            trainer = Trainers.objects.filter(active_status = True,batch__academic_counsellor__profile=request.user)


            if query :

                trainer=Trainers.objects.filter(Q(active_status=True)&Q(batch__academic_counsellor__profile=request.user)&(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(post_office__icontains=query)|Q(contact__icontains=query)|Q(pin_code__icontains=query)|Q(house_name__icontains=query)|Q(email__icontains=query)|Q(course__name__icontains=query)|Q(batch__name__icontains=query)|Q(district__icontains=query)))
        else:

             trainer = Trainers.objects.filter(active_status = True)

             print(query)

             if query:

                 trainer= Trainers.objects.filter(Q(active_status=True)&(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(course__name__icontains=query)))

        # students = Students.objects.all()
        
        print(trainer)

        data = {'trainers':trainer,'query':query}

        return render(request,'trainers/trainer.html',context=data)
    

@method_decorator(permission_roles(roles=["ADMIN","SALES"]),name='dispatch')

class TrainerRegistrationView(View):

    def get(self,request,*args,**kwargs):

        form  = TrainerRegisterForm()

        data = {'form':form}

        # data = {'districts':DistrictChoices,'courses':CourseChoices,'batches':Batch,'trainers':TrainerName,'form':form}

        # data ={"numbers ": [1,2,3,4,5]}

        return render(request,'trainers/registerform.html',context=data)
    
    def post(self,request,*args,**kwargs):
        
        form = TrainerRegisterForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

              trainer = form.save(commit=False)

              trainer.adm_number = get_employee_number()

              username=trainer.email

              password=get_password()

              profile= Profile.objects.create_user(username=username,password=password,role='trainer')

              trainer.profile=profile

             # trainer.join_date = '2025-02-05'

              trainer.save()

            return redirect('trainers-list')
        
        else :
            data = {'form':form}

            return render (request,'trainers/registerform.html',context=data)
        

        
       

    #     form_data = request.POST
    
    #     first_name = form_data.get("first_name")
    #     last_name = form_data.get("last_name")
    #     photo = request.FILES.get("photo")
    #     email = form_data.get("email")
    #     contact_number = form_data.get("contact_number")
    #     house_name = form_data.get("house_name")
    #     post_office = form_data.get("post_office")
    #     pincode = form_data.get("pincode")
    #     course = form_data.get("course")
    #     district = form_data.get("district")
    #     batch = form_data.get("batch")
    #     batch_date = form_data.get("batch_date")
    #     trainer = form_data.get("trainer")

    #     adm_number = get_admission_number()

    #     join_date ='2024-08-16'

    #     print(adm_number)

    #     print(first_name)
    #     print(last_name)
    #     print(email)
    #     print(contact_number)
    #     print(house_name)
    #     print(post_office)
    #     print(pincode)
    #     print(course)
    #     print(district)
    #     print(batch)
    #     print(batch_date)
    #     print(trainer)

    #     Students.objects.create(first_name=first_name,
    #                            last_name=last_name,
    #                            photo=photo,
    #                            email=email,
    #                            contact = contact_number,
    #                            house_name = house_name,
    #                            post_office=post_office,
    #                            district = district,
    #                            pincode = pincode,
    #                            adm_number=adm_number,
    #                            course=course,
    #                            batch=batch,
    #                            batch_date=batch_date,
    #                            trainer_name = trainer,
    #                            join_date=join_date


    #                         )

        
    
    # context={'first_name':first_name,'last_name':last_name,'photo':photo,'email':email,'contact_number':contact_number,'house_name':house_name,'post_office':post_office,'pincode':pincode,'course':course,'districts':district,'batch':batch,'batch_date':batch_date,'trainer':trainer})
    
# class CourseView(View) :

#     def get(self,request,*args,**kwargs):

#         return render(request,'students/course.html')
# class BatchView(View) :

#     def get(self,request,*args,**kwargs):

#         return render(request,'students/course.html')    

# @method_decorator(permission_roles(roles=["ADMIN","SALES"]),name='dispatch')

class TrainerDetailView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        # pk = kwargs.get('pk')

        # student = get_object_or_404(Students,pk=pk)

        trainer = GetTrainerObject().get_trainer(request,uuid)



        # try:

        #    student = Students.objects.get(pk=pk)

        #    print(student)

        # except:

        #     return redirect('error-404')

        data ={'trainer':trainer}

        return render(request,'trainers/trainer-detail.html',context=data)

    
# student delete view
# @method_decorator(permission_roles(roles=["ADMIN","SALES"]),name='dispatch')

class TrainerDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        # pk=kwargs.get('pk')

        # try :

        #     student = Students.objects.get(pk=pk)

        # except :

        #     return redirect('error-404')
        
        trainer =GetTrainerObject().get_trainer(request,uuid)

        # student.delete()

        trainer.active_status = False
        trainer.save()

        return redirect('trainers-list')

# @method_decorator(permission_roles(roles=["ADMIN","SALES"]),name='dispatch')

class TrainerUpdateView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        # pk = kwargs.get('pk')

        trainer = GetTrainerObject().get_trainer(request,uuid)

        # student = GetStudentObject().get_student(pk)

        form = TrainerRegisterForm(instance=trainer)

        data = {'form' : form}

        return render(request,'trainers/trainer-update.html',context=data)
    
    def post(self,request,*args,**kwargs):


        # pk = kwargs.get('pk')

        uuid = kwargs.get('uuid')

        trainer = GetTrainerObject().get_trainer(request,uuid)

        # student = GetStudentObject().get_student(pk)

        form = TrainerRegisterForm(request.POST,request.FILES,instance=trainer)

        if form.is_valid():

            form.save ()

            return redirect('trainers-list')
        
        else :

            data = {'form' :form}

            return render(request,'trainers/trainer-update.html',context=data)


