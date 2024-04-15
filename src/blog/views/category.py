from django.shortcuts import get_object_or_404
from django.views.generic import *

from ..models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = "blog/index.html"
    ordering = "-date_created"
    extra_context = {"page_title": "СТАТЬИ", "background_image": "blog/assets/img/home-bg.jpg"}

    def get_heading(self):
        return get_object_or_404(Category, slug=self.kwargs.get("category_slug")).name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["heading"] = self.get_heading()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category__slug=self.kwargs.get("category_slug"))

    def get_ordering(self):
        ordering = self.request.GET.get("orderBy")

        if ordering is not None and (
                (ordering.startswith("-") and hasattr(self.model, ordering[1:]))
                or hasattr(self.model, ordering)
        ):
            return ordering
        else:
            return self.ordering


class AboutTemplateView(TemplateView):
    template_name = "blog/about.html"
    extra_context = {
        "page_title": "ABOUT",
        "background_image": "blog/assets/img/about-bg.jpg",
        "heading": "ABOUT US"
    }


class ArticleDetail(DetailView):
    slug_url_kwarg = "article_slug"
    template_name = "blog/post.html"
    model = Article
    context_object_name = "article"
    extra_context = {"background_image": "blog/assets/img/post-bg.jpg"}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["heading"] = self.object.title
        return context
