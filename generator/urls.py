from django.urls import path

from . import views

urlpatterns = [
    path("generate/", views.generate_content_view, name="generate"),
    path("content/<int:pk>/", views.content_detail, name="content_detail"),
    path("content/<int:pk>/edit/", views.content_edit, name="content_edit"),
    path("content/<int:pk>/seo/", views.analyze_seo_view, name="analyze_seo"),
    path("content/<int:pk>/grammar/", views.grammar_check_view, name="grammar_check"),
    path("content/<int:pk>/image/", views.generate_image_view, name="generate_image"),
    path("content/<int:pk>/export/<str:fmt>/", views.export_content, name="export_content"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("calendar/<int:pk>/delete/", views.calendar_delete, name="calendar_delete"),
    path("history/", views.history_view, name="history"),
]
