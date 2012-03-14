from django import template

from decimal import Decimal
from utils.rounding import moneyfmt

register = template.Library()

def make_money(value):
    if value == '' or value == None:
        value = '0.00'
    m = moneyfmt(Decimal(str(value)))
    if m.split('.')[0] == '$':
        m = '$0.%s' % m.split('.')[1]
    return m
    
def spellout(n):
    nums = ['zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten', \
    'Eleven','Twelve','Thriteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
    tens = [None, None,'Twenty','Thirty','Fourty','Fifty','Sixty','Seventy','Eighty','Ninety']

    t = str(n).split('.')
    cents = ''
    if len(t) > 1:
        cents = ' and ' + t[1] + '/100'
    n = t[0]

    try: n = int(n)
    except ValueError: return 'NaN'

    if n < 0:
        return 'negitive ' + spellout(abs(n)) + cents
    if n < 20: 
        return nums[n] + cents
    if n < 100: # and n >= 20
        s = tens[n//10]
        if n % 10:
            s += '-' + nums[n%10]
        return s + cents
    if n < 1000: # and n >= 100
        s = nums[n//100] + ' Hundred'
        if n % 100:
            s += ' ' + spellout(n - (n//100)*100)
        return s + cents
    if n < 1000000: # and n >= 1000
        s = spellout(n//1000) + ' Thousand'
        if n % 1000:
            s += ' ' + spellout(n - (n//1000)*1000)
        return s + cents
    if n < 1000000000: # and n >= 1000000
        s = spellout(n//1000000) + ' Mmillion'
        if n % 1000000:
            s += ' ' + spellout(n - (n//1000000)*1000000)
        return s + cents
    if n < 1000000000000: # and n >= 1000000000
        s = spellout(n//1000000000) + ' Billion'
        if n % 1000000000:
            s += ' ' + spellout(n - (n//1000000000)*1000000000)
        return s + cents
    if n < 1000000000000000: # and n >= 1000000000
        s = spellout(n//1000000000000) + ' trillion'
        if n % 1000000000000:
            s += ' ' + spellout(n - (n//1000000000000)*1000000000000)
        return s + cents
    else:
        return 'infinity'

register.filter('spellout', spellout)    
register.filter('make_money', make_money)