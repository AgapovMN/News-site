from email.policy import default
from django.db import models
from django.forms import ImageField
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length = 150, verbose_name = 'Заголовок')
    content = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата публикации')
    updated_at = models.DateTimeField(auto_now = True)
    photo = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank = True)
    is_published = models.BooleanField(default = True)
    category = models.ForeignKey('Category', on_delete = models.PROTECT, null = True, 
    verbose_name = 'Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['id']
    
    def get_absolute_url(self):
        return reverse('view_news', kwargs = {'news_id': self.id})

class Category(models.Model):
    title = models.CharField(max_length = 150, db_index = True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.title