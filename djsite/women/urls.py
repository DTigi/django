from django.urls import path, register_converter, include
from . import views, converters
from rest_framework import routers


# router = routers.DefaultRouter() # или кастомный MyCustomRouter из routers.py
# router.register(r"women", views.WomenViewSet, basename='women')

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.WomenHome.as_view(), name="home"),  # http://127.0.0.1:8000/
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("login/", views.login, name="login"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path("blog/", views.blog, name="blog"),
    path("category/<slug:cat_slug>/", views.WomenCategory.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", views.TagPostList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit_page"),
    path("delete/<slug:slug>/", views.DeletePage.as_view(), name="edit_page"),
    # path("api/v1/", include(router.urls)),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path("api/v1/women/", views.WomenAPIList.as_view()),
    path("api/v1/women/<int:pk>/", views.WomenAPIUpdate.as_view()),
    path("api/v1/womendelete/<int:pk>/", views.WomenAPIDelete.as_view()),
]
