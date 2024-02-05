from django import forms
from allauth.account.forms import SignupForm,PasswordField
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from allauth.utils import set_form_field_order

from django.forms.widgets import ClearableFileInput, CheckboxInput


class ImageWidget(ClearableFileInput):
    template_name = "widgets/image_widget.html"

class MyCustomSignupForm(SignupForm):
    mobile = forms.RegexField(
        label="मोबाईल नम्बर",
        widget=forms.TextInput(
            attrs={"placeholder": "Mobile"}
        ),
        regex="^\\d+$",
        min_length=10,
        max_length=10
    )
    first_name= forms.CharField(
        label="First Name",
    )
    last_name= forms.CharField(
        label="Last Name",
    )
    
    field_order = ["mobile","username","first_name","last_name","email", "password1","password2"]
        
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
                label="मोबाईल नम्बर",
                widget=forms.TextInput(
                    attrs={"placeholder": "मोबाईल नम्बर"}
                ),
            )
    password = PasswordField(label="पासवर्ड", autocomplete="current-password")
    
    field_order = ["username",  "password"]
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, ["username", "password"])
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = ({
                    'first_name': 'नाम',
                    'last_name': 'थर',
                    'email': 'ई-मेल',
                })
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone','city','country','organization','photo', 'bio' ]
        labels = ({
                    'phone': 'मोबाइल नं.',
                    'city': 'नगरपालिका / गाउँपालिका',
                    'country': 'देश',
                    'organization': 'संस्था (जागिर खाने भएमा)',
                    'photo': 'प्रोफाईल फोटो',
                    'bio': 'आफ्नो बारेमा लेख्नुहोस',
                })
        
        widgets = {
            'bio': forms.Textarea(attrs={'rows':3}),
            'photo':ImageWidget(),
            'country': forms.TextInput(attrs={'value':"नेपाल"}) ,
        }

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
    # expiry_date = forms.DateField(
    #     widget=forms.TextInput(
    #         attrs={'type': 'date','required':False}

    #     )
    # )
    # image = forms.ImageField(label='Image')

    class Meta:
        model = Item
        fields = ('title','category','price','has_discount','discount_price','available','unit','home_delivery','price_negotiable','show_expiry','expiry_date','description')
        exclude = ('likes', 'user', 'sold', 'hit_count_generic', 'featured')
        labels = ({
                    'title': 'बेच्ने सामानको नाम',
                    'price': 'मूल्य',
                    'has_discount': 'डिस्काउन्ट दिन सकिने',
                    'discount_price': 'डिस्काउन्ट पछिको मूल्य',
                    'category': 'वर्ग / समूह ',
                    'available': 'उपलब्ध परिमाण',
                    'unit': 'उपलब्ध परिमाणको ईकाई',
                    'home_delivery': 'होम डेलिभरी सम्भव छ',
                    'show_expiry': 'यो विज्ञापन देखाउने',
                    'price_negotiable': 'मूल्य घटाउन सकिने',
                    'description': 'आफ्नो सामानको बारेमा लेख्नुहोस',
                    'expiry_date': 'विज्ञापन कहिले सम्म देखाउने ?',
                    'image': 'सामानको फोटोहरु',
                })

        widgets = {
            'expiry_date': forms.DateInput(attrs={'type':'date','required':False}),
            'description': forms.Textarea(attrs={'rows':3}),
            'has_discount': forms.CheckboxInput(attrs={'onclick':"toggleDiscountField()"}),
            'unit': forms.Select(attrs={'required':True}),
        }
        # fields = ['title', 'price', 'discount_price', 'category', 'available', 'unit',
        #   'home_delivery', 'price_negotiable', 'description', 'image', 'expiry_date', 'featured']

    def __init__(self, *args, **kwargs):
        super(AdditemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name in ['title','category','available','unit']:
                visible.field.widget.attrs['col']='col-md-6'
            elif visible.name in ['price','has_discount','discount_price']:
                visible.field.widget.attrs['col']='col-md-4'
            elif visible.name in ['home_delivery','price_negotiable','show_expiry','expiry_date']:
                visible.field.widget.attrs['col']='col-md-3'
            elif visible.name in ['description']:
                visible.field.widget.attrs['col']='col-md-12 my-3'
            else:
                visible.field.widget.attrs['col'] = 'col-md-4' 

class ImageForm(forms.ModelForm):
    image = forms.ImageField(
    label='फोटोहरु<sub>(१ वा १ भन्दा बढी)<sub>', widget=ImageWidget(attrs={'multiple': True}))

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