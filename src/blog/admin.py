from django.contrib import admin
from django.db.models import Model, QuerySet
from django.http import HttpRequest

from .models import Article, Category


@admin.action(description="Опубликовать")
def make_publish(modeladmin: Model, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_published=True)


@admin.action(description="Снять с публикации")
def make_unpublish(modeladmin: Model, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_published=False)


class ArticleStackedInline(admin.StackedInline):
    model = Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published")
    list_filter = ("category", "is_published")
    date_hierarchy = "date_created"
    actions = (make_publish, make_unpublish)
    prepopulated_fields = {
        "slug": ("title", "category")
    }
    fieldsets = [
        (
            "Основные",
            {
                "fields": ["title", "category", "body"]
            },
        ),
        (
            "Дополнительные",
            {
                "classes": ["collapse"],
                "fields": ["is_published", "slug"]
            },
        )
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", )
    # list_editable = ("name", )
    save_as = True
    prepopulated_fields = {
        "slug": ("name", )
    }
    inlines = (ArticleStackedInline,)
