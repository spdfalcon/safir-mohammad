from django.conf import settings
from products.models import Package, Course, Part
from django.contrib import messages

class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()

        # Get the package objects and add them to the cart
        package_ids = [pid for pid in product_ids if self.cart[pid]['product_type'] == 'package']
        packages = Package.objects.filter(id__in=package_ids)
        for package in packages:
            product_id = str(package.id)
            self.cart[product_id]['product'] = package

        # Get the course objects and add them to the cart
        course_ids = [pid for pid in product_ids if self.cart[pid]['product_type'] == 'course']
        courses = Course.objects.filter(id__in=course_ids)
        for course in courses:
            product_id = str(course.id)
            self.cart[product_id]['product'] = course
        
        # Get the part objects and add them to the cart
        part_ids = [pid for pid in product_ids if self.cart[pid]['product_type'] == 'part']
        parts = Part.objects.filter(id__in=part_ids)
        for part in parts:
            product_id = str(part.id)
            self.cart[product_id]['product'] = part

        # Update prices and calculate total price
        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product_id, quantity=1, product_type='package'):
        product = None
        try:
            if product_type == 'package':
                product = Package.objects.get(id=product_id)
            elif product_type == 'course':
                product = Course.objects.get(id=product_id)
            elif product_type == 'part':
                product = Part.objects.get(id=product_id)
            else:
                raise ValueError("Invalid product type")
            
        except (Package.DoesNotExist, Course.DoesNotExist, Part.DoesNotExist):
            messages.error(self.request, "محصول مورد نظر یافت نشد.")
            return

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_id': product.id,
                'product_slug': product.slug,
                'product_title': product.title,
                'product_image_url': product.image.url,
                'price': str(product.price_with_discount if product.price_with_discount else product.price),
                'quantity': 0,
                'product_type': product_type,
            }

        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_count(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())
