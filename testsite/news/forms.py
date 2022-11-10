from django import forms
from .models import Category

class NewsForm(forms.Form):
    title = forms.CharField(max_length = 150, label = 'Заголовок', widget = forms.TextInput({'class': 'form-control'}))
    content = forms.CharField(label = 'Текст', widget = forms.Textarea({'class': 'form-control', 'rows': 5}))
    is_published = forms.BooleanField(label = 'Опубликовать', initial = True)
    category = forms.ModelChoiceField(queryset = Category.objects.all(), label = 'Категория', empty_label = 'Выберите категорию', widget = forms.Select({'class': 'form-control'}))

