import pytest

from meallogger.models import Meal


def test_user_can_post_meal_successfully(base_mealtracker_fixture, django_app):
    # Pre conditions
    assert Meal.objects.count() == 0

    index = django_app.get('/', user=base_mealtracker_fixture['testuser'])
    form = index.form
    form['mealtime'] = 'lunch'
    form['item'] = 'apple'
    form['quantity'] = 1
    form['unit'] = 'small'
    response = form.submit().follow()

    # Post conditions
    assert Meal.objects.count() == 1

    messages_div = response.html.find('div', class_='alert alert-success')
    assert messages_div is not None


def test_posted_meal_in_usermeals_page(
        base_mealtracker_fixture, base_submit_form_fixture, django_app):
    response = django_app.get(
        '/testuser/', user=base_mealtracker_fixture['testuser'])
    assert response.status_int == 200

    all_td_tags = response.html.find_all('td')
    food_item = [td.text for td in all_td_tags if td.text == 'apple']
    assert food_item == ['apple']


def test_correct_date_filter_in_usermeals_page(
        base_mealtracker_fixture, base_submit_form_fixture, django_app):
    index = django_app.get(
        '/testuser/', user=base_mealtracker_fixture['testuser'])
    date_form = index.forms[0]
    date_form['req_date'] = '2018-05-28'
    response = date_form.submit()

    all_td_tags = response.html.find_all('td')
    food_item = [td.text for td in all_td_tags if td.text == 'apple']
    assert food_item == ['apple']


def test_wrong_date_filter_in_usermeals_page(
        base_mealtracker_fixture, base_submit_form_fixture, django_app):
    index = django_app.get(
        '/testuser/', user=base_mealtracker_fixture['testuser'])
    date_form = index.forms[0]
    date_form['req_date'] = '2018-05-30'
    response = date_form.submit()

    all_td_tags = response.html.find_all('td')
    food_item = [td.text for td in all_td_tags if td.text == 'apple']
    assert food_item != ['apple']


def test_delete_meal_in_usermeals_page(
        base_mealtracker_fixture, base_submit_form_fixture, django_app):
    index = django_app.get(
        '/testuser/', user=base_mealtracker_fixture['testuser'])
    response = index.clickbutton(description='delete', verbose=True)

    all_td_tags = response.html.find_all('td')
    food_item = [td.text for td in all_td_tags if td.text == 'apple']
    assert food_item == []
