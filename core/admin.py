from django.contrib import admin
from .models import *


class ImagesAdmin(admin.StackedInline):
    model = Images


class ItemAdmin(admin.ModelAdmin):
    inlines = [ImagesAdmin]

    class Meta:
        model = Item
    search_fields = ('title',)
    list_filter = ('featured', 'category', 'upload_date',)


class ImagesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
admin.site.register(Images, ImagesAdmin)

admin.site.register(Order)
admin.site.register(categories)

admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(aboutpage)
admin.site.register(subscripiton)

admin.site.register(Partner)
admin.site.register(PoweredBy)
admin.site.register(UserProfile)
