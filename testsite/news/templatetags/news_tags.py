from django import template
from news.models import Category
from django.db.models import Count
from django.core.cache import cache

register = template.Library()

#@register.simple_tag()
#def get_category():
    #return Category.objects.all() - Simole tag

@register.inclusion_tag("news/list_categoryes.html")
def show_category():
    category = cache.get('category')
    if not category:
        category = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
        cache.set('category', category, 30)
    return{'category':category}

