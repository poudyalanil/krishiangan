from .models import *
from django.forms.models import modelformset_factory
from .forms import *
from django.forms.models import inlineformset_factory


def custom_processor(request):
    category = categories.objects.all()

    if request.user.is_authenticated:
        postform = AdditemForm()
        pknew = request.user.id
        user_form = UserForm(instance=request.user)
        profile_id = UserProfile.objects.filter(user=request.user).first()
        userformset = UserProfileForm(instance=profile_id)
        
        partners = Partner.objects.filter(is_active=True).order_by('display_order')
        powered_by = PoweredBy.objects.filter(is_active=True).order_by('display_order').first()

        return {'postForm': postform, "noodle": pknew,
                "noodle_form": user_form,
                "userformset": userformset, 
                'categories': category,
                'partners': partners,
                'powered_by': powered_by,
                }
    else:
        return {'categories': category,
                'partners': partners,
                'powered_by': powered_by,}
