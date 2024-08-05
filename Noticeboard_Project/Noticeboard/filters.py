from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Notice


class NoticeFilter(FilterSet):

    added_after = DateTimeFilter(
        field_name='date_posted',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Notice

        fields = {

            'title': ['icontains'],
            'category': ['exact'],

        }