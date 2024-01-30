from django.contrib import admin
from .models import *


class ImagesAdmin(admin.StackedInline):
    model = Images


class ItemAdmin(admin.ModelAdmin):
    inlines = [ImagesAdmin]

    class Meta:
        model = Item
    search_fields = ('title',)
    list_display = ('title', 'category', 'available','unit','price','sold','discount_price','home_delivery','price_negotiable','user','upload_date','expiry_date')
    list_filter = ('user','category','featured','upload_date','price_negotiable','home_delivery')


class ImagesAdmin(admin.ModelAdmin):
    class Meta:
        model = Images
    list_display = ('item','image')


class StaffsAdmin(admin.ModelAdmin):
    class Meta:
        model = Staffs
    list_display = ('name_en','name_lc', 'post_en','post_lc','display_order','is_active')
    
class AboutPageAdmin(admin.ModelAdmin):
    class Meta:
        model = aboutpage()
    list_display = ('main_title','bottom_title')
    
class PageSectionsAdmin(admin.ModelAdmin):
    class Meta:
        model = PageSections
    list_display = ('title','content', 'image','is_for_bottom_section','display_order','is_active')

class PartnerAdmin(admin.ModelAdmin):
    class Meta:
        model = Partner
    list_display = ('name_en','name_lc', 'url','logo_url','display_order','is_active')
    
class PoweredByAdmin(admin.ModelAdmin):
    class Meta:
        model = PoweredBy
    list_display = ('name_en','name_lc', 'url','logo_url','display_order','is_active')
    
class UnitAdmin(admin.ModelAdmin):
    class Meta:
        model = Unit
    list_display = ('title_en','title_lc','display_order','is_active')
    
    
admin.site.register(Unit, UnitAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Images, ImagesAdmin)

admin.site.register(Order)
admin.site.register(categories)

admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(aboutpage,AboutPageAdmin)   
admin.site.register(PageSections,PageSectionsAdmin)
admin.site.register(Staffs,StaffsAdmin)
admin.site.register(subscripiton)
admin.site.register(Partner,PartnerAdmin)
admin.site.register(PoweredBy,PoweredByAdmin)
admin.site.register(UserProfile)
