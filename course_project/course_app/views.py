from django.contrib.auth.models import User
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import *
from .forms import *
# Create your views here.


# Register
def user_signup(request):

    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            user=User.objects.create_user(username=username,email=email,password=pass1)
            user.save()
            return redirect('login')
        
    return render (request,'signup.html')

# Login
def user_login(request):
    
    if request.user.is_authenticated:
        print('user is authenticated')
        return redirect('course_list')
    
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username,password=password)
        print(user,'-------------user---')
        if user is not None:
            login(request, user)
            print('----------------logged in-------')
            return redirect('course_list')
            

        return HttpResponse("Invalid Credentials!!")
    return render(request,'login.html')

# Shows the courselist
@login_required(login_url = 'login')
def course_list(request):
    keyword = request.GET.get('keyword')
    courses = Course.objects.all()
    if keyword:
        courses = courses.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(keywords__icontains=keyword))
    
    paginator = Paginator(courses, 2)  # Display 2 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/course_list.html', {'page_obj': page_obj})

# Create a new course
@login_required(login_url='login')
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})


# Update course Method
def update_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/update_course.html', {'form': form, 'course': course})

# Delete a Course
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/delete_course.html', {'course': course})


# Change password
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('course_list')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


# Logout
@login_required(login_url ='login')
def user_logout(request):
    logout(request)
    return redirect('/')

