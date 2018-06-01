from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Meal(models.Model):
    MEALTIME_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('brunch', 'Brunch'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner'),
        ('late snack', 'Late Snack'),
    )
    UNIT_OF_MEASURES = (
        ('ounces', 'oz'),
        ('grams', 'g'),
        ('small', 'small'),
        ('medium', 'medium'),
        ('large', 'large'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    mealtime = models.CharField(
        max_length=12,
        choices=MEALTIME_CHOICES,
        default='Breakfast',
    )
    item = models.CharField(max_length=20, default='')
    quantity = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(20), MinValueValidator(1)],
    )
    unit = models.CharField(
        max_length=8,
        default='oz',
        choices=UNIT_OF_MEASURES,
    )
    calories = models.FloatField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
