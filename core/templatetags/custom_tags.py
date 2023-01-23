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

@register.filter
def convertToNepali(input):
    return str(input).replace(',',',').replace('.','.').replace('0','०').replace('1','१').replace('2','२').replace('3','३').replace('4','४').replace('5','५').replace('6','६').replace('7','७').replace('8','८').replace('9','९')
    

@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__ 