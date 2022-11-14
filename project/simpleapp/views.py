# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Product, Category  # Дополнительно импортируем категорию, чтобы пользователь мог её выбрать
from datetime import datetime

from django.shortcuts import render
from django.views import View  # импортируем простую вьюшку
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод

from .filters import ProductFilter  # импортируем недавно написанный фильтр
'''
# Create your views here.
class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    # model = Product
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'name'
    queryset = Product.objects.order_by('name')
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = 'Sale on Tuesday!'
        return context


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
'''
'''
# В отличие от дженериков, которые мы уже знаем, код здесь надо писать самому, переопределяя типы запросов (например гет или пост, вспоминаем реквесты из модуля C5)
class Products(View):

    def get(self, request):
        products = Product.objects.order_by('-price')
        p = Paginator(products, 1)  # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы

        products = p.get_page(request.GET.get('page', 1))  # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами

        data = {
            'products': products,
        }
        return render(request, 'product_list.html', data)
    '''


class Products(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 20  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса, отправленного на сервер
        name = request.POST['name']
        quantity = request.POST['quantity']
        category_id = request.POST['category']
        price = request.POST['price']

        product = Product(name=name, quantity=quantity, category_id=category_id,
                          price=price)  # создаём новый товар и сохраняем
        product.save()
        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.
