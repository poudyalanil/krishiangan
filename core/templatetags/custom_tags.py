from django import template
import json
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

@register.filter(name='is_odd')
def is_odd(value):
    return value % 2 != 0

nepali_numbers = {
    '0': '०',
    '1': '१',
    '2': '२',
    '3': '३',
    '4': '४',
    '5': '५',
    '6': '६',
    '7': '७',
    '8': '८',
    '9': '९',
}

def convert_to_nepali_numbers(value):
    return ''.join(nepali_numbers.get(char, char) for char in str(value))

register.filter('nepali_numbers', convert_to_nepali_numbers)


english_numbers = {
     '०' :'0',
     '१' :'1',
     '२' :'2',
     '३' :'3',
     '४' :'4',
     '५' :'5',
     '६' :'6',
     '७' :'7',
     '८' :'8',
     '९' :'9',
}

def convert_to_english_numbers(value):
    return ''.join(english_numbers.get(char, char) for char in str(value))

register.filter('english_numbers', convert_to_english_numbers)

@register.filter
def messages_to_json(messages):
    """
    Convert Django messages to a JSON-formatted string.
    """
    return json.dumps([{'message': str(message),'type':message.tags} for message in messages])
