import pytest


@pytest.fixture
def base_mealtracker_fixture(django_app, django_user_model):
    testuser = django_user_model.objects.create_user(
        username='testuser', email='testuser@example.com', password='12345')
    return {'testuser': testuser}


@pytest.fixture
def authenticated_user(base_mealtracker_fixture, django_app):
    testuser = base_mealtracker_fixture['testuser']
    form = django_app.get('/').form
    form['username'] = testuser.username
    form['password'] = '12345'
    resp = form.submit().follow()

    assert resp.status_code, "Couldn't authenticate user"

    return base_mealtracker_fixture


@pytest.fixture
def base_submit_form_fixture(base_mealtracker_fixture, django_app):
    index = django_app.get('/', user=base_mealtracker_fixture['testuser'])
    form = index.form
    form['mealtime'] = 'lunch'
    form['item'] = 'apple'
    form['quantity'] = 1
    form['unit'] = 'small'
    response = form.submit().follow()

    return {'response': response}
