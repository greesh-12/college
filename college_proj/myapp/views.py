from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from .models import *
import os
from django.contrib.auth.decorators import login_required
# Create your views here.
def loginpage(request):
    return render(request,'loginpage.html')

def login_func(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_home')
            else:
                login(request,user)
                auth.login(request,user)
                return redirect('user_home')
        else:
            messages.info(request,'Invalid Username or Password')
            return redirect('loginpage')
    return render(request,'reg.html')

@login_required(login_url='loginpage')
def admin_home(request):
    return render(request,'admin_home.html')



def reg(request):
    c=Course.objects.all()
    return render(request,'reg.html',{'course':c})

def user_create(request):
    if request.method=='POST':
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        usrname=request.POST['username']
        address=request.POST['address']
        age=request.POST['age']
        email=request.POST['email']
        phone=request.POST['phone']
        pswd=request.POST['password']
        cpswd=request.POST['confirm_password']
        image=request.FILES.get('img')
        course=request.POST['course']
        c1=Course.objects.get(id=course)
        if pswd==cpswd:
            if User.objects.filter(username=usrname).exists():
                messages.info(request,'username already exist')
                return redirect('reg')
            else:
                usr=User.objects.create_user(first_name=fname,last_name=lname,username=usrname,email=email,password=pswd)
                usr.save()
                u=User.objects.get(id=usr.id)
                tr=Teacher.objects.create(user=u,address=address,age=age,phone=phone,image=image,course=c1)
                tr.save()

        else:
            messages.info(request,'password does not match')
            return redirect('reg')
        return redirect('loginpage')

def log_out(request):
    auth.logout(request)
    return redirect('loginpage')

@login_required(login_url='loginpage')
def course(request):
    return render(request,'course.html')


def add_course(request):
    if request.method=='POST':
        course_name=request.POST['course_name']
        course_fees=request.POST['course_fees']
        course=Course(coursename=course_name,fees=course_fees)
        course.save()
        return redirect('add_stud')
    
@login_required(login_url='loginpage')
def add_stud(request):
    c=Course.objects.all()
    return render(request,'add_stud.html',{'course':c})

def add_student(request):
    if request.method=='POST':
        name=request.POST['student_name']
        address=request.POST['address']
        age=request.POST['age']
        doj=request.POST['doj']
        course=request.POST['course']
        c1=Course.objects.get(id=course)
        student=Student(course=c1,studentname=name,address=address,age=age,joiningdate=doj)
        student.save()
        return redirect('stud_details')
    
@login_required(login_url='loginpage')
def stud_details(request):
    student=Student.objects.all()
    return render(request,'stud_details.html',{'stud':student})

@login_required(login_url='loginpage')
def edit(request,id):
    student=Student.objects.get(id=id)
    c=Course.objects.all()
    return render(request,'edit.html',{'stud':student,'course':c})

def edit_details(request,id):
    if request.method=='POST':
        std=Student.objects.get(id=id)
        std.studentname=request.POST['student_name']
        std.address=request.POST['address']
        std.age=request.POST['age']
        std.joiningdate=request.POST['doj']
        c=request.POST['course']
        c1=Course.objects.get(id=c)
        std.course=c1
        std.save()
        return redirect('stud_details')
    return render(request,'edit.html')

@login_required(login_url='loginpage')
def delete(request,id):
    student=Student.objects.get(id=id)
    student.delete()
    return redirect('stud_details')

@login_required(login_url='loginpage')
def teacher_details(request):
    teacher=Teacher.objects.all()
    return render(request,'teacher_details.html',{'tr':teacher})

def delete_tchr(request,id):
    tt=Teacher.objects.get(id=id)
    user = tt.user
    tt.delete()
    user.delete()
    return redirect('teacher_details')

@login_required(login_url='loginpage')
def user_home(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    return render(request,'user_home.html',{'teacher': teacher,'user': user,})

@login_required(login_url='loginpage')
def card(request):
        tchr=Teacher.objects.get(user=request.user)
        cr=Course.objects.all()
        return render(request,'card.html',{'tcr':tchr,'csr':cr})

@login_required(login_url='loginpage')
def edit_teacher(request):
    
    tch=Teacher.objects.get(user=request.user)
    crcs=Course.objects.all()
    return render(request,'edit_teacher.html',{'tchr':tch, 'courses':crcs})

def edit_tr(request,id):
    if request.method=='POST':
        t=Teacher.objects.get(user=id)
        user=User.objects.get(id=id)
        user.first_name=request.POST['fname']
        user.last_name=request.POST['lname']
        user.username=request.POST['uname']
        t.address=request.POST['add']
        t.age=request.POST['age']
        user.email=request.POST['mail']
        t.phone=request.POST['phone']
        courseid=request.POST['c']
        course=Course.objects.get(id=courseid)
        t.course=course
        new_image=request.FILES.get('img')
        if new_image:
            if t.image:
                os.remove(t.image.path)
                t.image = new_image
        t.save()
        user.save()
        return redirect('card')
    return render(request,'edit_teacher.html')
