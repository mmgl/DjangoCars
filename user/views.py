from django.conf import Settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.checks import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from car.models import Category, Comment, Car
from home.models import UserProfile, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm
from user.models import CarForm


@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile
               }
    return render(request, 'user_profile.html', context)

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
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    category = Category.objects.all()
    context = {'comments': comments,
               'category': category,
               'profile': profile}
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def delete_comment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Yorumunuz silinmiştir.')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def add_content(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            catid = form.cleaned_data['category']
            data = Car()
            data.category_id = catid.id
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
            data.status = 'New'
            data.user_id = current_user.id
            data.save()
            messages.success(request, "Photo successfully added.")
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, "Please correct the errors: " + str(form.errors))
            return HttpResponseRedirect('/user/add_content')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = CarForm()
        context = {'setting': setting,
                   'category': category,
                   'form': form
                   }
        return render(request, 'add_content.html', context)