from ckeditor.widgets import CKEditorWidget
from django.db import models

# Create your models here.
from django.forms import ModelForm, Select, TextInput, FileInput

from car.models import Car, Category, Images


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['category', 'title', 'slug', 'keywords', 'description', 'image','price','year','fuel','gear','km','motor','color', 'detail']
        widgets = {
            'category': Select(attrs={'class': 'input', 'placeholder': 'category'}, choices=Category.objects.all()),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Başlık'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'fiyat'}),
            'year': TextInput(attrs={'class': 'input', 'placeholder': 'Yıl'}),
            'fuel': TextInput(attrs={'class': 'input', 'placeholder': 'Yakıt Türü'}),
            'gear': TextInput(attrs={'class': 'input', 'placeholder': 'Vites'}),
            'km': TextInput(attrs={'class': 'input', 'placeholder': 'Km'}),
            'motor': TextInput(attrs={'class': 'input', 'placeholder': 'Motor Gücü'}),
            'color': TextInput(attrs={'class': 'input', 'placeholder': 'Renk'}),
            'detail': CKEditorWidget(),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
        }


class CarImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']