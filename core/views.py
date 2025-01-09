import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, RedirectView

from PIL import Image

from .models import Prediction, PredictionLabel


API_URL = 'https://studious-waffle-4vvw6jvx5w4fj774-8000.app.github.dev'


class PredictCreateView(LoginRequiredMixin, CreateView):
    template_name = 'core/predict_new.html'
    model = Prediction
    fields = ['image']

    def get_success_url(self):
        return reverse_lazy('core:predict_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        prediction = form.save(commit=False)
        prediction.created_by = self.request.user
        image_file = form.cleaned_data['image']

        response = requests.post(f'{API_URL}/predict', files={'data': image_file.file})
        response.raise_for_status()
        preds = response.json()
        prediction.save()

        prediction_labels = []
        for pred in preds:
            label, confidence = pred['label'], round(pred['confidence'] * 100, 3)
            prediction_labels.append(
                PredictionLabel(
                    prediction=prediction,
                    label=label,
                    confidence=confidence
                )
            )
        PredictionLabel.objects.bulk_create(prediction_labels)
        return super(PredictCreateView, self).form_valid(form)


class PredictDetailView(LoginRequiredMixin, DetailView):
    template_name = 'core/predict_detail.html'
    model = Prediction
    context_object_name = "prediction"

    def get_queryset(self):
        return self.model.objects.prefetch_related('labels').select_related('created_by').filter(created_by=self.request.user)


class PredictionHistoryView(LoginRequiredMixin, ListView):
    template_name = 'core/prediction_history.html'
    model = Prediction
    context_object_name = 'predictions'
    paginate_by = 10
    ordering = '-created_at'

    def get_queryset(self):
        self.queryset = self.model.objects.prefetch_related('labels').select_related('created_by').filter(created_by=self.request.user)
        return super(PredictionHistoryView, self).get_queryset()


class PredictionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'core/prediction_delete.html'
    model = Prediction
    success_url = reverse_lazy('core:prediction_history')

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)


class HomeRedirectView(RedirectView):
    url = reverse_lazy('core:predict_form')