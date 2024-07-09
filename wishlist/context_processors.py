from .models import Wishlist

def wishlist_count(request):
    if not request.user.is_authenticated:
        wishlist_count = 0
    else:
        try:
            wishlist = Wishlist.objects.filter(user=request.user).last()
            if wishlist:
                wishlist_count = wishlist.items.count()
            else:
                wishlist_count = 0
        except Exception as e:
            # Handle any exceptions here and set a default value
            wishlist_count = 0

    return {'wishlist_count': wishlist_count}