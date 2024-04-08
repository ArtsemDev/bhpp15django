from django.db import models
from django.core.validators import MinLengthValidator


class Category(models.Model):
    name = models.CharField(
        max_length=16,
        db_column="name",  # название колонки в БД (если не указать используется название атрибута)
        db_comment="category name",  # комментарий атрибута в БД,
        # db_default="",  # значение по умолчанию со стороны БД
        # default="",  # значение по умолчанию со стороны Django ORM,
        verbose_name="категория",
        unique=True,
        validators=(  # список/кортеж дополнительных валидаторов значения атрибута
            MinLengthValidator(limit_value=2),
        ),
        help_text="Название категории"  # текст подсказка (для формы создания),
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,  # уникальность значения
        verbose_name="URL",
        help_text="URL категории",
        allow_unicode=True,
        validators=(
            MinLengthValidator(limit_value=2),
        ),
        db_index=False,  # генерировать ли SQL Index на основании данного атрибута
        null=False,  # NOT NULL
        blank=False,  # разрешаем ли мы пустое значение как валидное
    )

    def __str__(self) -> str:
        return self.name  # noqa

    class Meta:
        verbose_name = "категория"  # удобочитаемое имя таблицы в ед.ч
        verbose_name_plural = "категории"  # удобочитаемое имя таблицы в мн.ч
        # abstract = True  # является ли данный класс абстракцией
        # db_table = "blog_category"  # название таблицы в БД
        # managed = False  # отключение управлением жизненным циклом таблицы
        # ordering = ["name", ]  # порядок сортировки по умолчанию
        # get_latest_by = "name"  # по какому измененному атрибуту будет определяться "последняя" запись
        # app_label = "blog"  # к какому приложение принадлежит таблица если описана за пределами приложения


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
    category = models.ForeignKey(  # НЕЛЬЗЯ указывать unique=True для достижения отношения 1to1, для этого используйте OneToOneField
        to=Category,  # на какую таблицы ссылаемся
        on_delete=models.PROTECT,  # ссылочная спецификация при удалении
        related_name="articles",  # название атрибута "с обратной стороны"
        related_query_name="article",  # название атрибута при построении запросов "с обратной стороны"
        db_index=True
    )

    def __str__(self) -> str:
        return self.title  # noqa

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["-date_created", ]  # "-" указывает на обратный порядок сортировки
