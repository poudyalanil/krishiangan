from .models import *
from django.forms.models import modelformset_factory
from .forms import *
from django.forms.models import inlineformset_factory


def custom_processor(request):
    category = categories.objects.all()
    powered_by = PoweredBy.objects.filter(is_active=True).order_by('display_order').first()
    social_media= SocialMedia.objects.filter(is_active=True).order_by('display_order')
    if request.user.is_authenticated:
        postform = AdditemForm()
        pknew = request.user.id
        user_form = UserForm(instance=request.user)
        profile_id = UserProfile.objects.filter(user=request.user).first()
        userformset = UserProfileForm(instance=profile_id)

        return {'postForm': postform, "noodle": pknew,
                "noodle_form": user_form,
                "userformset": userformset, 
                'categories': category,
                'powered_by': powered_by,
                'social_media': social_media,
                }
    else:
        return {'categories': category,
                'powered_by': powered_by,
                'social_media': social_media,
                }
