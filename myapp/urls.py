from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sunburst/$', views.ChartView.as_view(), name='myapp'),
    url(r'^creditinfo/$', views.IndexView.as_view(), name='myapp'),
]