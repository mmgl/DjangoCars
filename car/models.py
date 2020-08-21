from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, FileInput, NumberInput, Select
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_up = models.DateTimeField(auto_now_add=True)
    update_up = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):  # alt kategori olduğu sürece alt kat arar
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])  # ard arda getirir


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'slug': self.slug})

class Car(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    year = models.IntegerField()
    fuel = models.CharField(max_length=20)
    gear = models.CharField(max_length=20)
    km = models.IntegerField()
    motor = models.IntegerField()
    color = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS)
    detail = RichTextUploadingField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Images(models.Model):
    Car = models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50,blank=True)
    comment = models.TextField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment']



class ContentForm(ModelForm):
    class Meta:
        model = Car
        fields = {'category','title','keywords','description','slug','image','price','year',
                  'fuel','gear','km','motor','color','detail'}
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Başlık'}),
            'category': Select(attrs={'class': 'input', 'placeholder': ''}, choices=Category.objects.all()),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'Slug'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'Keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'Resim'}),
            'price': NumberInput(attrs={'class': 'input', 'placeholder': 'Fiyat'}),
            'year': NumberInput(attrs={'class': 'input', 'placeholder': 'Yıl'}),
            'fuel': TextInput(attrs={'class': 'input', 'placeholder': 'Yakıt'}),
            'gear':TextInput(attrs={'class': 'input', 'placeholder': 'Vites'}),
            'km':NumberInput(attrs={'class': 'input', 'placeholder': 'Kilometre'}),
            'motor':NumberInput(attrs={'class': 'input', 'placeholder': 'Motor Gücü'}),
            'color': TextInput(attrs={'class': 'input', 'placeholder': 'Renk'}),
            'detail': CKEditorWidget(),
        }

