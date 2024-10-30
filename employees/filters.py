import django_filters
from .models import Employee


class EmployeesFilter(django_filters.FilterSet):
    desgination = django_filters.CharFilter(field_name="desgination", lookup_expr="iexact")
    name = django_filters.CharFilter(field_name="emp_name", lookup_expr="icontains")
    # range function works on integer field 
    id = django_filters.RangeFilter(field_name="id")
    id_min = django_filters.CharFilter(method='filter_by_id_range', label='From EMP ID')
    id_max = django_filters.CharFilter(method='filter_by_id_range', label='To EMP ID')


    class Meta:
        fields = ['desgination', "name", "id", "id_min"]
        model = Employee

    def filter_by_id_range(self, queryset, name, value):
        if name == 'id_min':
            return queryset.filter(emp_id__gte=value)
        elif name == 'id_max':
            return queryset.filter(emp_id__lte=value)
        return queryset

