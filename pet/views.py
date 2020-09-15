from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from .models import Pet


class PetListPage(ListView):

    model = Pet

    def get_queryset(self):
        qs = super().get_queryset()
        get_params = self.request.GET.dict()

        if get_params.get('q'):
            qs = qs.filter(name__icontains=get_params.get('q'))

        return qs


class PetPage(DetailView):
    
    model = Pet


class ContactPage(TemplateView):
    template_name = "contacts.html"


class AboutPage(TemplateView):
    template_name = "about.html"