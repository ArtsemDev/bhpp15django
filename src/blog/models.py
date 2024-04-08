from django.db import models
from django.core.validators import MinLengthValidator


class Category(models.Model):
    name = models.CharField(
        max_length=16,
        verbose_name="категория",
        unique=True,
        validators=(
            MinLengthValidator(limit_value=2),
        ),
        help_text="Название категории"
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name="URL",
        help_text="URL категории",
        allow_unicode=True,
        validators=(
            MinLengthValidator(limit_value=2),
        ),
        db_index=False,
    )

    def __str__(self) -> str:
        return self.name  # noqa

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        # abstract = True  # является ли данный класс абстракцией
        # db_table = "blog_category"  # название таблицы в БД
        # managed = False  # отключение управлением жизненным циклом таблицы
        # ordering = ["name", ]
        # get_latest_by = "name"
        # app_label = "blog"


class Article(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name="заголовок",
        help_text="Заголовок статьи",
        validators=(
            MinLengthValidator(limit_value=5),
        )
    )
    slug = models.SlugField(
        max_length=128,
        verbose_name="URL",
        help_text="URL статьи",
        unique=True,
        validators=(
            MinLengthValidator(limit_value=5),
        ),
        allow_unicode=True,
        db_index=False
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        auto_now_add=True  # автоматическое определение даты при создании
    )
    date_updated = models.DateTimeField(
        verbose_name="дата изменения",
        auto_now=True  # автоматическое определение даты при сохранении (редактировании)
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name="articles",
        related_query_name="article",
    )

    def __str__(self) -> str:
        return self.title  # noqa

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["-date_created", ]
