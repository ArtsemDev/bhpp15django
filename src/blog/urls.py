from django.urls import path

from .views import category

urlpatterns = [
    path("about/", category.AboutTemplateView.as_view(), name="blog-about"),
    path("<slug:category_slug>/", category.ArticleListView.as_view(), name="article-list"),
    path("<slug:category_slug>/<slug:article_slug>/", category.ArticleDetail.as_view(), name="article-detail")
]
