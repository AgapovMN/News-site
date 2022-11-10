from django.shortcuts import render
from .models import News, Category
from django.http import Http404
from .forms import NewsForm
from django.shortcuts import redirect

def main_page(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': "Список новостей",
    }
    return render(request, 'news/mainpage.html', context = context)
    
def get_category(request, category_id):
    news = News.objects.filter(category_id = category_id)
    category = Category.objects.get(id = category_id)
    return render(request, 'news/category.html', {'news': news,'category': category})

def view_news(request, news_id):
    try:
        news_item = News.objects.get(pk = news_id)
    except News.DoesNotExist:
        raise Http404('Страница не найдена')
    return render(request, 'news/view_news.html', {'news_item': news_item})

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = News.objects.create(**form.cleaned_data)
            return redirect(news)
    else:
        form = NewsForm()
        return render(request, 'news/add_news.html', {'form': form})