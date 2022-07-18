from django import template
register = template.Library()


@register.filter_function
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter_function
def filter_category(queryset, filter):
    return queryset.filter(category=filter)


@register.filter_function
def filter_featured(queryset, filter):
    return queryset.filter(featured=True)
