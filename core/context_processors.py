from .models import *
from django.forms.models import modelformset_factory
from .forms import *
from django.forms.models import inlineformset_factory


def custom_processor(request):
    category = categories.objects.all()

    if request.user.is_authenticated:

        ImageFormSet = modelformset_factory(Images,
                                            form=ImageForm
                                            )
        postform = AdditemForm()
        postformset = ImageFormSet(queryset=Images.objects.none())
        pknew = request.user.id
        user_form = UserForm(instance=request.user)
        profile_id = UserProfile.objects.filter(user=request.user).first()
        userformset = UserProfileForm(instance=profile_id)
        # ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
        #     'phone', 'city', 'country', 'organization', 'photo',  'bio',))
        # userformset = ProfileInlineFormset(instance=request.user)

        return {'postForm': postform, 'formset': postformset, "noodle": pknew,
                "noodle_form": user_form,
                "userformset": userformset, 'categories': category}
    else:
        return {'categories': category}
