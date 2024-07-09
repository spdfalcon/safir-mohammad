from django import template


register = template.Library()

@register.filter
def split_price(price):
    """
    Custom template filter to split the price into groups of three numbers.
    """
    price_str = str(price)
    parts = []
    while price_str:
        parts.append(price_str[-3:])
        price_str = price_str[:-3]
    return ','.join(reversed(parts))

@register.filter
def get_selected_package_ids(order):
    return order.items.values_list('package__id', flat=True)

@register.filter
def get_selected_course_ids(order):
    return order.items.values_list('course__id', flat=True)

@register.filter
def get_selected_part_ids(order):
    return order.items.values_list('part__id', flat=True)


