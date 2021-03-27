from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls.static import static
from django.template.exceptions import TemplateDoesNotExist
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'