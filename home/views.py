import json

from django.contrib.auth import logout, authenticate, login
from django.core.checks import messages
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from car.models import Category, Car, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:5] #slider a 5 adet ürün getirdik
    category = Category.objects.all()
    daycars = Car.objects.all()[:5]
    lastcars = Car.objects.all().order_by('-id')[:5]
    randomcars = Car.objects.all().order_by('?')[:5]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'daycars': daycars,
               'lastcars': lastcars,
               'randomcars': randomcars,
               }
    return render(request, "index.html", context)


def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category}
    return render(request, 'hakkimizda.html', context)


def referans(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category}
    return render(request, 'referans.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir.")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactFormu()

    context = {'setting': setting,
               'form': form,
               'category': category}
    return render(request, 'iletisim.html', context)


def category_cars(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    if slug == 'child':
        cars = Car.objects.filter(category_id=id)
    else:
        cars = Car.objects.filter(category__parent_id=id)

    context = {'cars': cars,
               'category': category,
               'categorydata': categorydata,
               'setting': setting}
    return render(request, 'car.html', context)


def car_detail(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    images = Images.objects.filter(Car_id=id)
    comments = Comment.objects.filter(car_id=id, status='True')
    car = Car.objects.get(pk=id)
    randomcars = Car.objects.all().order_by('?')[:4]
    setting = Setting.objects.get(pk=1)
    context = {'car': car,
               'category': category,
               'randomcars': randomcars,
               'comments': comments,
               'categorydata': categorydata,
               'images': images,
               'setting': setting}
    return render(request, 'car_detail.html', context)


def car_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            cars = Car.objects.filter(title__icontains=query)
            setting = Setting.objects.get(pk=1)
            context = {'cars': cars,
                       'category': category,
                       'setting': setting}
            return render(request, 'car_search.html', context)
    return HttpResponseRedirect('/')


def car_search_auto(request):
        if request.is_ajax():
            q = request.GET.get('term', '')
            cars = Car.objects.filter(title__icontains=q)
            results = []
            for pl in cars:
                cars_json = {}
                cars_json = pl.city + "," + pl.state
                results.append(cars_json)
            data = json.dumps(results)
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.Warning(request, "Login Hatası ! Kullanıcı adı veya şifre hatalı!")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'setting' : setting}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request,username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/avatar01.png"
            data.save()
            messages.success(request, "Üye Kaydı Alınmıştır")
            return HttpResponseRedirect('/')
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form}
    return render(request, 'signup.html', context)



