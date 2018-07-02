import requests

from django.views import View
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate

from meallogger.models import Meal
from meallogger.forms import MealForm, CustomSignUpForm


class HomeView(View):

    model = Meal
    form_class = MealForm
    template_name = 'meal.html'
    APP_ID = '{{ api id }}'
    APP_KEY = '{{ api key }}'
    API_URL = ('https://api.edamam.com/api/nutrition-data?app_id={app_id}'
               '&app_key={app_key}&ingr={qty}%20{unit}%20{item}')

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        return render(request, 'meal.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            username = str(request.user)
            calories = self._query_api_for_calories(request.POST)
            meal = self.model(
                username=username,
                mealtime=form.cleaned_data['mealtime'],
                item=form.cleaned_data['item'],
                quantity=form.cleaned_data['quantity'],
                unit=form.cleaned_data['unit'],
                calories=calories)
            meal.save()
            messages.success(request, 'Meal Successfully Added!')
            return redirect('/')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def _query_api_for_calories(self, payload):
        quantity = payload.get('quantity')
        unit_type = payload.get('unit')
        food_item = payload.get('item')
        resp = requests.get(self.API_URL.format(
            app_id=self.APP_ID,
            app_key=self.APP_KEY,
            qty=quantity,
            unit=unit_type,
            item=food_item))
        return eval(resp.text.encode('utf-8')).get('calories', 0)


class UserMeals(View):

    model = Meal
    template_name = 'usermeals.html'

    @method_decorator(login_required)
    def get(self, request, username):
        if str(request.user).lower() != username.lower():
            return HttpResponseForbidden()

        if request.GET.get('delete'):
            self.model.objects.filter(id=request.GET.get('delete')).delete()

        date = request.GET.get('req_date', '')
        context = self._get_context(username, date)
        return render(request, self.template_name, context)

    def _get_context(self, username, date):
        return {
            'username': username.title(),
            'meals_list': self.model.objects.filter(
                username__icontains=username,
                timestamp__contains=date).all(),
            'total_cals': self.model.objects.filter(
                username__icontains=username,
                timestamp__contains=date).aggregate(
                    Sum('calories')).get('calories__sum'),
        }


class SignUpView(View):

    form_class = CustomSignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})
