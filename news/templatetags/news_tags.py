from django import template

from news.models import Category
from django.db.models import Count, F
from django.core.cache import cache


register = template.Library() #регистрация категории


@register.simple_tag(name='get_list_categories') # Декораторы
def get_categories():
    return Category.objects.all() #возвращение всех категорий

@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1=' Hello', arg2 = 'World'):
    # categories = cache.get('categories') #если есть в кэше пытаемся оттуда получить данные
    # if not categories:
    #     categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    #     #если нет, то мы их получаем из базы данных и кладем в кэш, при следующем обращении, если не прошло 30
    #     # секунд, они будут
    #     cache.set('categories', categories, 30)

    # categories = Category.objects.all()

    #отфильтровал через F и убрал отображение в сумме неопубликованных новостей (неактивных)
    #убрал ту категорию где 0 новостей
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {"categories": categories, "arg1": arg1, 'arg2': arg2}