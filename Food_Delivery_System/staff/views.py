from django.shortcuts import render
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
# Create your views here.


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        # get the current date
        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        total_income = 0
        for order in orders:
            total_income += order.price

        context = {
            'orders': orders,
            'income': total_income,
            'total_orders': len(orders)
        }
        return render(request, template_name='staff/dashboard.html', context=context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }
        return render(request, template_name='staff/order-details.html', context=context)

    def post(self, request, pk):
        order = OrderModel.objects.get(pk=pk)
        order.is_delivered = True
        order.save()
        context = {
            'order': order
        }
        return render(request, template_name='staff/order-details.html', context=context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()