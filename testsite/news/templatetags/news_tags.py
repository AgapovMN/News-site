from django import template
from news.models import Category

register = template.Library()

#@register.simple_tag()
#def get_category():
    #return Category.objects.all() - Simole tag

@register.inclusion_tag("news/list_categoryes.html")
def show_category():
    category = Category.objects.all()
    return{'category':category}

