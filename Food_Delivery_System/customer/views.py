from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.contrib import messages

from .models import MenuItem, OrderModel


# Create your views here.
class Order(View):
    def get(self, request):
        carbohydrates = MenuItem.objects.filter(category__name__contains='carbohydrate')
        proteins = MenuItem.objects.filter(category__name__contains='protein')
        soft_drinks = MenuItem.objects.filter(category__name__contains='soft drink')
        beverage_drinks = MenuItem.objects.filter(category__name__contains='beverage drink')
        vitamins = MenuItem.objects.filter(category__name__contains='vitamins')
        snacks = MenuItem.objects.filter(category__name__contains='snack')
        context = {
            'carbs': carbohydrates,
            'prots': proteins,
            'soft': soft_drinks,
            'beverage': beverage_drinks,
            'vitamins': vitamins,
            'snacks': snacks,
        }
        return render(request, template_name='customer/order.html', context=context)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        county = request.POST.get('county')
        sub_county = request.POST.get('sub-county')
        area = request.POST.get('area')
        order_items = {
            'items': []
        }
        items = request.POST.getlist('items[]')
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            if menu_item.price == '':
                messages.error(request, message='Please select a dish')
                return redirect(to='order/')
            else:
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.name,
                    'price': menu_item.price
                }
                order_items['items'].append(item_data)

                price = 0
                item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        order = OrderModel.objects.create(
            price=price,
            first_name=first_name,
            second_name=second_name,
            email=email,
            county=county,
            sub_county=sub_county,
            area=area,
        )
        order.items.add(*item_ids)
        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order_confirmation', pk=order.pk)

    
class OrderConfirmation(View):
    def get(self, request, pk):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }
        return render(request, 'customer/confirmation.html', context=context)

    def post(self, request):
        pass

class Menu(View):
    def get(self, request):
        menu_items = MenuItem.objects.all()
        context = {
            'menu_items': menu_items
        }
        return render(request, template_name='customer/menu.html', context=context)


class MenuSearch(View):
    def get(self, request):
        query = self.request.GET.get('q')
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )
        context = {
            'menu_items': menu_items
        }
        return render(request, 'customer/menu.html', context)


class Payment(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        print(phone_number)