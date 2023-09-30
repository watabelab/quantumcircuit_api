from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), #urlに/app/indexと入力するとviews.pyのindex関数が呼び出される。(nameは他のテンプレートからviewを呼び出す際に用いるが、この記事では無関係)
]