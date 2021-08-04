from django.db import models
from django.urls import reverse


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True,
                               verbose_name='Контент')  # Бланк тру значит что можно будет с пустой строкой сохранить
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')  # Будет записана текущая дата создания новости и больше заменяться не будет
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено')  # Обновление новости и постоянно обновляется дата и будем видеть когда последний раз редактировалась новость
    photo = models.ImageField(
        upload_to='photos/%y/%m/%d/', verbose_name='Фото',
        blank=True)  # загружать файлы (только картинки_) и куда их сохранять, по указанному пути и разбиваем файлф по дате загрузки, чтбы не захламлять директорию
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')  # Новость по умолчанию публикуется
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 verbose_name='Категория', )  # в кавычках потому что класс
    views = models.IntegerField(default=0)
    # определен позже,
    # если б раньше то можно без кавычек

    # он делейт - тут указал защиту от удаления связанных данных. Не забывать регистрировать ее, это важно. в админ пай

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'  # наименование модели в единственном числе
        verbose_name_plural = 'Новости'  # наименование модели в множественном числе
        ordering = ['-created_at']  # сортировка


class Category(models.Model):
    objects = None
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title  # теперь новость можно добавлять не в странные категории, а в наука\спорт и тд

    class Meta:
        verbose_name = 'Категория'  # наименование модели в единственном числе
        verbose_name_plural = 'Категории'  # наименование модели в множественном числе
        ordering = ['title']  # сортировка
