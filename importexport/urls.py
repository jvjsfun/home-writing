
from django.urls import path
from .import views


urlpatterns = [
    path("login_prontopro/", views.login_prontopro, name="login_prontopro"),
    path("send_data_to_sheet/<phpsessid>/<int:profile>/",
         views.send_data_to_sheet, name="send_data_to_sheet"),
    path("send_snippets/<int:profile>/<int:id_snippet>/",
         views.send_snippets, name="send_snippets"),
    path("pop/", views.pop, name="pop"),
    path("get_all_snippets/", views.get_all_snippets, name="get_all_snippets"),
    path("read_snippets/<int:profile>/",
         views.read_snippets, name="read_snippets"),
    #path("set_timesleep/", views.set_timesleep, name="set_timesleep")
    path("cancel_all_snippets/", views.cancel_all_snippets, name="cancel_all_snippets"),
]
