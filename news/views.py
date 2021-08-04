from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .models import News, Category
from .forms import NewsForm , UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView #задача данного класса вернуть какой то список(к №1)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .utils import MyMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #сохраняю регистрацию и
            login(request, user) #сразу его авторизую
            messages.success(request, 'Nuts!')
            return redirect('home')
        else:
            messages.error(request, 'error registration')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST) #без  этого ('data=') работать не будет
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'test_djangovich@mail.ru',
            ['nxcu1xgjhjph@mail.ru'], fail_silently= False)
            if mail:
                messages.success(request, 'E-mail sent!')
                return redirect('contact')
            else:
                messages.error(request, 'sent error') #редирект не делается чтобы остался на странице
        else:
            messages.error(request, 'error validation')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


class HomeNews(ListView): #это класс подкласса лист вью
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news' #вместо обжект_лист будем работать с ньюс и таким образом на главной странице все
    # отображается
    #extra_context = {'title': 'Главная'} #отображается на шапке страницы, желательно ехтраконтекс использовать для
    # статичных данных, для списков и динамичных данных не стоит. Мы ее переопределили внизу
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) #в переменную контекст записали все что было в гет сонтекст
        # дата, теперь мы ее дополняем
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published = True).select_related('category') #убирает неопубликованные новости,
        # но пока только с главной
        # страницы

class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False #не разрешаем показ пустых списков или в нашем случае несуществующих страниц
    paginate_by = 2
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) #в переменную контекст записали все что было в гет сонтекст
        # дата, теперь мы ее дополняем
        context['title'] = Category.objects.get(pk=self.kwargs['category_id']) #номер запрошенной категории выводится
        # в верху страница
        return context
    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News #данные получаем из таблицы новостей
    context_object_name = "news_item"
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id' #урл собирается из данныъ ньюс айди

class CreateNews(LoginRequiredMixin, CreateView):
    #надо связать данный класс с классом формы
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #success_url = reverse_lazy('home')
    #login_url = reverse_lazy('home') #перебрасывает, если я неавторизованный пытаюсь зайти в добавить новость
    raise_exception = True



#def index(request):
    #Хранятся в севозможные данные о клиенте, его браузере, куки, данные сессии и т.д
    #print((dir(request))) здесь куча инфы высвечивается о все что только можно о клиенте, куки те же самые и т.д
#    news = News.objects.all() #Сортировка по полю в обратном порядке order_by('-created_at')
#    context = {'news': news, "title": 'Список новостей', }
#    return render(request, template_name='news/index.html', context = context)
    # как рендерить шаблон. 1 парметром рекуест , вторым параметорм название шаблона (путь к темплайт
    # по умолчанию стоит. 3 параметром контекст. Можно то что в фигурных скобках, в новую переменную включить
    # если много инфы, например в context = {}

# def get_category(request, category_id):
#     news= News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news,  "category": category})


# def view_news(request, news_id, news_item=None):
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

# def add_news(request): #принимаект объект запроса
#     if request.method == 'POST': #если данные приходят постом
#         form = NewsForm(request.POST) #эта форма связана с данными
#         if form.is_valid(): #тут что то связаненое с валидацией, если через код браузера удаляют рекуаред
#            # print(form.cleaned_data)
#             #news = News.objects.create(**form.cleaned_data) # ** = распаковка словарей
#             news = form.save() # это автор говорит идентично верхнему
#             return redirect(news)
#     else:
#         form = NewsForm() #а эта не связана и остаются при ошибке все данные которые пользовател вводил
#     return render(request, 'news/add_news.html', {'form': form})