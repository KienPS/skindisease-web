from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import User


class Prediction(models.Model):
    image = models.ImageField(upload_to='images/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name


class PredictionLabel(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='labels')
    label = models.CharField(max_length=255)
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
