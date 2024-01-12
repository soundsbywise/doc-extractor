from django.urls import path

from . import views

urlpatterns = [
    # maps the index URL for this app to the extract view handler
    path("", views.extractInvestmentStatement,
         name="extractInvestmentStatement"),
]
