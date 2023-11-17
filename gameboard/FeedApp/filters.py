from django_filters import FilterSet
from .models import Reply


class PostFilter(FilterSet):
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Reply
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'post': ['exact'],
        }
