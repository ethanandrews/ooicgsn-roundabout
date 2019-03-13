from django.urls import path

from . import views

app_name = 'admintools'
urlpatterns = [
    path('printers/', view=views.PrinterListView.as_view(), name='printers_home'),
    path('printers/add/', view=views.PrinterCreateView.as_view(), name='printers_add'),
]
