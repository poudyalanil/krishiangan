from django import forms

from .models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# class AddCommentForm(forms.ModelForm):

#     class Meta:
#         model = Comment
#         fields = [
#             'Item',
#             'name',
#             'body',
#             'user'
#         ]


class AdditemForm(forms.ModelForm):
    expiry_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}

        )
    )
    # image = forms.ImageField(label='Image')

    class Meta:
        model = Item
        exclude = ('likes', 'user', 'sold', 'hit_count_generic', 'featured')

        # fields = ['title', 'price', 'discount_price', 'category', 'available', 'unit',
        #   'home_delivery', 'price_negotiable', 'description', 'image', 'expiry_date', 'featured']

    def __init__(self, *args, **kwargs):
        super(AdditemForm, self).__init__(*args, **kwargs)
        # self.fields['thumbnail'].required = False


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Images
        fields = ('image', )


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = subscripiton
        fields = ('email',)


# make separate form for admin panel and staff
class CategoriesAdminForm(forms.ModelForm):
    class Meta:
        model = categories
        fields = '__all__'


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = categories
        exclude = ['client', ]


class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['client', ]


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['client', ]


class OrderItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['client', ]
