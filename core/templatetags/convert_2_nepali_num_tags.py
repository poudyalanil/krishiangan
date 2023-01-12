from django import template

register = template.Library()

@register.filter
def convertToNepali(input):
    return str(input).replace(',',',').replace('.','.').replace('0','०').replace('1','१').replace('2','२').replace('3','३').replace('4','४').replace('5','५').replace('6','६').replace('7','७').replace('8','८').replace('9','९')
    
