

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from car.models import Category, Comment, Car
from home.models import Setting, UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm
from user.models import CarForm




@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               'setting': setting
               }
    return render(request, 'user_profile.html', context)



@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil bilgileriniz güncellenmiştir!')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')

        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form,
            'category': category})


@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {'comments': comments,
               'category': category,
               }
    return render(request, 'user_comments.html', context)



@login_required(login_url='/login')
def delete_comment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Yorumunuz silinmiştir.')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Car()
            data.user_id = current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.price = form.cleaned_data['price']
            data.year = form.cleaned_data['year']
            data.fuel = form.cleaned_data['fuel']
            data.gear = form.cleaned_data['gear']
            data.km = form.cleaned_data['km']
            data.motor = form.cleaned_data['motor']
            data.color = form.cleaned_data['color']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.save()
            messages.success(request, "İçerik Eklendi.")
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, "Form hatası: " + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = CarForm()
        context = {'setting': setting,
                   'category': category,
                   'form': form
                   }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login')
def contents(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               }
    return render(request, 'user_contents.html', context)


@login_required(login_url='/login') #check login
def contentedit(request,id):
    content = Category.objects.get(id=id) #category geliyor
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance =content)
        if form.is_valid():
            form.save()
            messages.success(request,'Your Content Updated Successfuly')
            return HttpResponseRedirect('/user/')
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit/' +str(id))
    else:
        category = Category.objects.all()
        form = CarForm(instance=content)
        context = {
            'category': category,
            'form': form,
        }
        return render(request,'user_addcontent.html',context)


@login_required(login_url='/login') #check login
def contentdelete(request,id):
    current_user = request.user
    Car.objects.filter(id=id, user_id = current_user.id).delete() #product silme
    messages.success(request, 'Product deleted..')
    return HttpResponseRedirect('/user/')