from asyncio.windows_events import NULL
from django.contrib import admin
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


# base custom model admin for filtering client data
class CustomModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        try:
            clientUser = ClientUser.objects.get(user=request.user.id)
        except ObjectDoesNotExist:
            clientUser = None

        # get superuser client id to show data inserted by superuser
        try:
            superClientUser = ClientUser.objects.get(Q(user__is_superuser=True))
        except ObjectDoesNotExist:
            superClientUser = None

        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(client_id=clientUser.client_id)| qs.filter(client_id=superClientUser.client_id)

    def save_model(self, request, obj, form, change):
        if request.user.is_staff:
            obj.client_id = ClientUser.objects.get(
                user=request.user.id).client_id
        super().save_model(request, obj, form, change)
        
        
class ImagesAdmin(admin.StackedInline):
    model = Images


class ItemAdmin(CustomModelAdmin):
    inlines = [ImagesAdmin]

    def get_form(self, request, obj=None, **kwargs):

        if request.user.is_superuser:
            return ItemAdminForm
        elif request.user.is_staff:
            return ItemForm

    class Meta:
        model = Item
    search_fields = ('title', 'category')
    list_filter = ('featured', 'category', 'upload_date','client')
    list_display = ('title', 'category', 'price',
                    'discount_price', 'available', 'client', 'user')


class ImagesAdmin(admin.ModelAdmin):
    pass

class ClientUserAdmin(admin.ModelAdmin):
    class Meta:
        model = ClientUser
    list_display = ('user', 'client')

class categoriesAdmin(CustomModelAdmin):
    
    def get_form(self, request, obj=None, **kwargs):

        if request.user.is_superuser:
            return CategoriesAdminForm
        elif request.user.is_staff:
            return CategoriesForm

    class Meta:
        model = categories
    list_display = ('category', 'client')
        
class OrderAdmin(CustomModelAdmin):
        
    def get_form(self, request, obj=None, **kwargs):

        if request.user.is_superuser:
            return OrderAdminForm
        elif request.user.is_staff:
            return OrderForm
    class Meta:
        model = Order
    list_display = ('user','ordered', 'ordered_date', 'client')
    
class OrderItemAdmin(CustomModelAdmin):
    
    def get_form(self, request, obj=None, **kwargs):
    
        if request.user.is_superuser:
            return OrderItemAdminForm
        elif request.user.is_staff:
            return OrderItemForm
    class Meta:
        model = OrderItem
    list_display = ('user','ordered', 'item','quantity','client')

admin.site.register(Client)
admin.site.register(ClientUser, ClientUserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(categories, categoriesAdmin)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Comment)
admin.site.register(aboutpage)
admin.site.register(subscripiton)


admin.site.register(UserProfile)