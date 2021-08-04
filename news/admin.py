from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import News, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm #подрубили админскую доп панель от скэдитор
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')  # настраивающий
    # класс
    list_display_links = ('id', 'title')  # ссылка рабоатет на каких кнопках
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')  # фильтр по каким категориям а также редактировать из админки
    fields = ('title', 'category', 'content', 'photo', 'get_photo',  'views', 'created_at',
              'updated_at')
    readonly_fields = ('get_photo','updated_at','views','created_at','updated_at')
    save_on_top = True #Кнопка сохранить наверху
    def get_photo(self, obj):

        if obj.photo:
            return mark_safe(f'<img src = "{obj.photo.url}" width = "75">')
        else:
            return 'no photo'

    get_photo.short_description = 'Miniature'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')  # настраивающий класс
    list_display_links = ('id', 'title')  # ссылка рабоатет на каких кнопках
    search_fields = ('title',)  # ставим запятую потому что тут кортеж иначе будет обычная строка


admin.site.register(News, NewsAdmin)  # регистрируем наше приложение + зарегестрировал класс НьюсАдмин
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'News management'
admin.site.site_header = 'News management'
