from django.shortcuts import render, redirect

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm

from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def user_send_mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'name@mail.ru', [form.cleaned_data['email']], fail_silently=True)
            if mail:
                messages.success(request, "Письмо отправлено")
                return redirect('send_mail')
            else:
                messages.error(request, "Ошибка! Письмо не отправлено!")
    else:
        form = ContactForm()
    return render(request, 'news/send_mail.html', {"form": form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрированы")
            return redirect('home')
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form":form})

def user_logout(request):
    logout(request)
    return redirect('login')

# def main_page(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': "Список новостей",
#     }
#     return render(request, 'news/mainpage.html', context = context)

class HomeNews(ListView):
    model = News
    template_name = 'news/mainpage.html'
    context_object_name = 'news'
    extra_content = {'title': 'Главная'}
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Главная'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published = True).select_related('category')


# def get_category(request, category_id):
#     news = News.objects.filter(category_id = category_id)
#     category = Category.objects.get(id = category_id)
#     return render(request, 'news/category.html', {'news': news,'category': category})


class GetCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published = True)


# def view_news(request, news_id):
#     try:
#         news_item = News.objects.get(pk = news_id)
#     except News.DoesNotExist:
#         raise Http404('Страница не найдена')
#     return render(request, 'news/view_news.html', {'news_item': news_item})

class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'
    # raise_exception = True

class Search(ListView):
    template_name = 'news/search.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(title__icontains = self.request.GET.get('s'))
    
    def get_context_data(self, *,object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context