from django import forms
from allauth.account.forms import SignupForm,LoginForm,PasswordField
from .models import *
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from allauth.utils import set_form_field_order
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect,get_object_or_404,redirect



class MyCustomSignupForm(SignupForm):
    mobile = forms.RegexField(
        label="Mobile",
        widget=forms.TextInput(
            attrs={"placeholder": "Mobile"}
        ),
        regex="^\\d+$",
        min_length=10,
        max_length=10
    )
    
    field_order = ["mobile","username","email", "password1","password2"]
        
    # def save(self, request):

    #     # Ensure you call the parent class's save.
    #     # .save() returns a User object.
    #     user_exists = User.objects.get(username=request.POST.get('mobile'))
    #     if(user_exists):
    #         messages.error(request,'Mobile no. already registered !!')
    #         return redirect('/accounts/signup')
    
    #     else:
    #         return
            # user = super(MyCustomSignupForm, self).save(request)
            # user_saved = User.objects.get(id=user.id)
            # user_saved.username = request.POST.get('mobile')
            # user_saved.save()
            # return user_saved
  
class MyCustomLoginForm(forms.Form):
    username = forms.CharField(
                label="Mobile",
                widget=forms.TextInput(
                    attrs={"placeholder": "Mobile"}
                ),
            )
    password = PasswordField(label="Password", autocomplete="current-password")
    
    field_order = ["username",  "password"]
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, ["username", "password"])
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'bio', 'phone','city','country','organization','user']

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


class BidItemForm(forms.ModelForm):
    class Meta:
        model=BidItem
        fields=['quantity','price'];