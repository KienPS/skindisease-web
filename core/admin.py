from django.contrib import admin

from .models import Prediction, PredictionLabel


class PredictionLabelInline(admin.TabularInline):
    model = PredictionLabel


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    inlines = [PredictionLabelInline]

