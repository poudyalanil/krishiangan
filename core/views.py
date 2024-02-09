from django.forms.models import inlineformset_factory
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, OrderItem, Order, Comment
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .serializers import *
from .forms import *
from hitcount.views import HitCountDetailView
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
import requests,time,random
from django.views.generic import ListView, DetailView, View, CreateView
from core.templatetags.custom_tags import convert_to_english_numbers
from django.forms.models import modelformset_factory
from allauth.account.views import PasswordResetView, PasswordResetFromKeyView

class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/custom_password_reset.html'

class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'account/custom_password_reset_from_key.html'


def account_reset_send_otp(request):
    if request.method == 'POST':
        mobile = request.POST['phone']
        user_profile = UserProfile.objects.filter(phone=mobile)
        
        if user_profile.exists():
            user_profile= user_profile.first()
            otp_code = generate_otp()
            # r = send_otp_via_sms(mobile, otp_code)
            status_code = 200
            if status_code == 200:
            # if r.status_code == 200:
                user_profile.otp_code = otp_code
                user_profile.valid_until = timezone.now() + timedelta(minutes=5)
                user_profile.save()
                messages.success(request, 'OTP is sent to the registered mobile number!!')
            else:
                messages.error(request, r.json().get('response', 'Failed to send OTP'))
        else:
            messages.error(request,'Sorry, we cannot find the records with provided infomation! \n Please contact Administrator !!')
            return redirect('core:account_reset_password')            
    return render(request,'main/otp_screen_for_reset.html',{'mobile_number':mobile});        


def account_reset_verify_otp(request):
    if request.method == 'POST':
        mobile = request.POST['mobile_number']
        verification_code = request.POST['verification_code']
        user_profile = UserProfile.objects.get(phone=mobile)
        user = user_profile.user
        if len(verification_code) == 6:
            if int(verification_code) == user_profile.otp_code:
                user_profile.otp_code = None
                user_profile.valid_until = None
                user_profile.save()
                messages.success(request,'Mobile Number is verified successfully !')
                return redirect('/')
            else:    
                messages.error(request,'Incorrect OTP Verification Code !')
                redirect(request.META.get('HTTP_REFERER'))
        else:
                messages.error(request,'OTP Verification Code does not match !')
                redirect(request.META.get('HTTP_REFERER'))
    return redirect('core:account_reset_password_from_otp')    
    
    
def accountSignup(request):
    username=request.POST.get('mobile')
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    user_exist = User.objects.filter(username=username)
    if(user_exist):
        messages.error(request,'Mobile no. already registered !!')
        # return redirect('/account/sign_up/')
        return redirect(reverse("account_signup"))
    else:
        if(request.POST.get('password1') != request.POST.get('password2')):
            messages.error(request,'Passord is not same !!')
            return redirect(reverse("account_signup"))

        else:
            user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=request.POST.get('email'),
                    password=request.POST.get('password1'),
                )
            return redirect("/accounts/login/")
    
def accountLogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # check if the username exist in database
    try:
        User.objects.filter(username=username)
    except:
        messages.error(request,'Username does not exist')

    # check the credential
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/")
    else:
        return redirect('/accounts/login/')

    
def HomeView(request):
    items = Item.objects.all()
    category = categories.objects.all()
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm
                                        )
    form = AdditemForm()
    formset = ImageFormSet(queryset=Images.objects.none())

    # user = User.objects.get(pk=request.user.id)
    if request.user.is_authenticated:

        pknew = request.user.id
        user_form = UserForm(instance=request.user)
        ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
            'phone', 'city', 'country', 'organization', 'photo',  'bio',))
        
        profile_id = UserProfile.objects.filter(user=request.user).first()
        userformset = UserProfileForm(instance=profile_id)

        return render(request, "main/index.html", {'items': items, 'categories': category, 'postForm': form, 'formset': formset, "noodle": pknew,
                                                   "noodle_form": user_form,"userformset": userformset, })
    else:
        return render(request, "main/index.html", {'items': items, 'categories': category, })
    
    
def updateUserProfile(request,pk):
    user = get_object_or_404(User,pk=pk)
    statuss = 'false'
    message='Some Error Occured !!'
    if(user):
        user.first_name =request.POST.get('first_name'); 
        user.last_name =request.POST.get('last_name'); 
        user.email =request.POST.get('email')
        user.save()
        user_profile = UserProfile.objects.get(user_id=pk)
        if(user_profile is None):
            user_profile = UserProfile
            user_profile.user_id=pk
        user_profile.bio = request.POST.get('bio')
        
        if user_profile.is_mobile_verified :
            if user_profile.phone != request.POST.get('phone'):
                messages.warning(request,'Verified Mobile number cannot be changed.\n Please Contact Administrator  !!' )
        else:    
            user_profile.phone = request.POST.get('phone')
            
        user_profile.city = request.POST.get('city')
        user_profile.country = request.POST.get('country')
        user_profile.organization = request.POST.get('organization')
        
        if(request.FILES):
            user_profile.photo = request.FILES['photo']
        else:
            user_profile.photo = user_profile.photo    
        user_profile.save()
        
        statuss='true'
        message='Profile successfully updated !!'
    return JsonResponse({'status':statuss,'message': message})

# Function to generate a unique 6-digit OTP
def generate_otp():
    # Get the current timestamp
    current_timestamp = int(time.time())
    # Generate a random component
    random_component = random.randint(100000, 999999)
    # Combine timestamp and random component to create the OTP
    otp = (current_timestamp % 1000000) * 1000000 + random_component

    return otp % 1000000  # Ensure the result is a 6-digit number


def send_otp_via_sms(mobile_number, otp_code):
    url = "http://api.sparrowsms.com/v2/sms/"
    token = "v2_kGCHEN8VopIfLY1xgDTsAf5CFlE.yfaD"
    message = f'Your OTP verification code is: {otp_code}'
    data = {'token': token, 'from': 'TheAlert', 'to': mobile_number, 'text': message}
    
    r = requests.post(url, data=data)
    return r

def send_otp_code(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = user.profile
        mobile_number = user_profile.phone

        if not user_profile.is_mobile_verified:
            if mobile_number:
                if user_profile.otp_code is None:
                    otp_code = generate_otp()
                    r = send_otp_via_sms(mobile_number, otp_code)
                    # r.status_code =200
                    if r.status_code == 200:
                        user_profile.otp_code = otp_code
                        user_profile.valid_until = timezone.now() + timedelta(minutes=5)
                        user_profile.save()
                        messages.success(request, 'OTP is sent to the registered mobile number!!')
                    else:
                        messages.error(request, r.json().get('response', 'Failed to send OTP'))
                else:
                    messages.info(request, 'OTP has already been sent to the registered mobile number. Please try after some time!!')
            else:
                messages.warning(request, 'Logged-in user does not have a mobile number!!')
        else:
            messages.info(request, 'The user\'s phone number is already verified!!')

    return redirect('/')

def verify_mobile(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = user.profile
        mobile_num = user_profile.phone
        
        #check if mobile number is nepali; convert if nepali
        mobile_num = convert_to_english_numbers(mobile_num) if not isinstance(mobile_num,int) else mobile_num
        masked_number = mobile_num[:1] + 'x'*6 + mobile_num[7:]
        
        if request.method == 'GET':
            if user_profile.is_mobile_verified:
                return redirect('/')
            return render(request,'main/otp_screen.html',{'masked_number':masked_number})
        else:    
            verification_code = request.POST['verification_code']
            if len(verification_code) == 6:
                if int(verification_code) == user_profile.otp_code:
                    user_profile.is_mobile_verified = True
                    user_profile.otp_code = None
                    user_profile.valid_until = None
                    user_profile.save()
                    messages.success(request,'Mobile Number is verified successfully !')
                    return redirect('/')
                else:    
                    messages.error(request,'Incorrect OTP Verification Code !')
            else:
                    messages.error(request,'OTP Verification Code does not match !')
        return redirect('core:verify_mobile_number')
       
                        
def subscribe(request):
    if request.method == 'POST':
        receiveForm = SubscriptionForm(request.POST)

        if receiveForm.is_valid():
            try:
                subs = subscripiton.objects.get(email=request.POST['email'])
                messages.info(request, "The provided email has already subscribed to our news letter !")
                return redirect('/')

            except:
                receiveForm.save()
                #also send message to user
                subject = 'Subscription-Krishiangan News Letter'
                from_email= settings.EMAIL_HOST_USER
                recipient_email=[request.POST['email']]
                base_url = settings.BASE_URL
                context={
                    'from_email':from_email,
                    'recipient_email':request.POST['email'],
                    'base_url':base_url
                }
                email_content = render_to_string('account/email/user_subscription.html',context)
                
                try:
                    send_mail(subject, '', from_email, recipient_email, html_message=email_content)
                    messages.success(request, "Successfully Subscribed !!")
                except BadHeaderError:
                    messages.info(request, "Invalid Header found !!")
                except Exception as e:
                    # Handle other exceptions (e.g., SMTP errors) here
                    messages.warning(request, "An error occurred while sending the email !!")
            return redirect('/')

def unsubscribe(request):
    email = request.GET['email']
    if email :
        record_exists = subscripiton.objects.filter(email=email)
        if record_exists.exists():
            record_exists.delete()
            
            subject = 'Unsubscription--Krishiangan News Letter'
            from_email= settings.EMAIL_HOST_USER
            recipient_email=[email]
            email_content = render_to_string('account/email/user_unsubscription.html')
            
            try:
                send_mail(subject, '', from_email, recipient_email, html_message=email_content)
                messages.success(request, "Successfully Unsubscribed !!")
            except BadHeaderError:
                messages.info(request, "Invalid Header found !!")
            except Exception as e:
            # Handle other exceptions (e.g., SMTP errors) here
                messages.warning(request, "An error occurred while sending the email !!")
        else:
            messages.info(request, "Sorry, the provided email information has no any active subscription !")
                
    return redirect('/')
    
    
def about(request):

    about_us = aboutpage.objects.first()
    about_sections = PageSections.objects.filter(is_active=True,is_for_bottom_section=False).order_by('display_order')
    staffs = Staffs.objects.filter(is_active=True).order_by('display_order')
    bottom_sections = PageSections.objects.filter(is_active=True,is_for_bottom_section=True).order_by('display_order')
  
    return render(request, "main/about.html", {
                                'about_us':about_us,
                                'about_sections':about_sections,
                                'bottom_sections':bottom_sections,
                                'staffs':staffs})
def partners(request):

    partners = Partner.objects.filter(is_active=True).order_by('display_order')

  
    return render(request, "main/partners.html", {'partners':partners})


def terms(request):

    category = categories.objects.all()
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm
                                        )
    form = AdditemForm()
    formset = ImageFormSet(queryset=Images.objects.none())
    # if request.user.is_authenticated:

    #     pknew = request.user.id
    #     user_form = UserForm(instance=request.user)
    #     ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
    #         'phone', 'city', 'country', 'organization', 'photo',  'bio',))
    #     userformset = ProfileInlineFormset(instance=request.user)

    #     return render(request, "main/terms_condition.html", {'categories': category, 'postForm': postform, 'formset': postformset, "noodle": pknew,
    #                                                          "noodle_form": user_form,
    #                                                          "userformset": userformset, })
    # else:
    return render(request, "main/terms_condition.html", {'categories': category, 'postForm': form, 'formset': formset})


class SearchResultsView(ListView):
    model = Item
    template_name = 'main/search_results.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        items = Item.objects.filter(Q(title__icontains=query))
        data['items'] = items
        return data


@login_required
def ItemLike(request, pk):
    item = get_object_or_404(Item, pk=pk)
    print(request.path_info)

    if item.likes.filter(id=request.user.id).exists():
        item.likes.remove(request.user)
        messages.info(request, "Your like removed from this item")

        return redirect('/')

    else:
        item.likes.add(request.user)
        messages.info(request, "Your like has been added ")
        return redirect("core:product", pk=pk)


def categoryview(request, pk):
    # categories = categories.objects.all()
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm
                                        )

    categoriestest = categories.objects.all()

    category = get_object_or_404(categories, pk=pk)
    items = Item.objects.filter(category=category)

    if request.user.is_authenticated:

        postform = AdditemForm()
        postformset = ImageFormSet(queryset=Images.objects.none())
        pknew = request.user.id
        user_form = UserForm(instance=request.user)
        ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
            'phone', 'city', 'country', 'organization', 'photo',  'bio',))
        # userformset = ProfileInlineFormset(instance=request.user)
        profile_id = UserProfile.objects.filter(user=request.user).first()
        userformset = UserProfileForm(instance=profile_id)
        

        return render(request, "main/category_page.html", {'items': items, 'categories': categoriestest, 'category': category, 'postForm': postform, 'formset': postformset, "noodle": pknew,
                                                           "noodle_form": user_form,
                                                           "userformset": userformset, })
    else:
        return render(request, "main/category_page.html", {'items': items, 'categories': categoriestest, 'category': category, })


class ItemDetailView(HitCountDetailView):
    model = Item
    count_hit = True
    template_name = "main/product-page.html"

    # def get(self, request, pk):
    #     category = categories.objects.all()
    #     item = get_object_or_404(Item, pk=pk)
    #     photos = Images.objects.filter(item=item)
    #     return render(request, "product-page.html", {'photos': photos, 'categories': category})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        items = Item.objects.all()

        likes_connected = get_object_or_404(Item, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        category = categories.objects.all()
        item = get_object_or_404(Item, pk=self.kwargs['pk'])
        photos = Images.objects.filter(item=item)
        ImageFormSet = modelformset_factory(Images,
                                            form=ImageForm
                                            )
        data['productbidlist'] = BidItem.objects.filter(item=self.kwargs['pk'],is_withdrawn=False)
        if self.request.user.is_authenticated:
            pknew = self.request.user.id
            user_form = UserForm(instance=self.request.user)
            ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
                'phone', 'city', 'country', 'organization', 'photo',  'bio',))
            # userformset = ProfileInlineFormset(instance=self.request.user)
            profile_id = UserProfile.objects.filter(user=self.request.user).first()
            userformset = UserProfileForm(instance=profile_id)
            
            biditemform = BidItemForm()
            postForm = AdditemForm()
            itemformset = ImageFormSet(queryset=Images.objects.none())
            data['noodle'] = pknew
            data['noodle_form'] = user_form
            data['userformset'] = userformset
            data['postForm'] = postForm
            data['biditemform'] = biditemform
            data['formset'] = itemformset
        data['categories'] = category
        data['photos'] = photos
        data['items'] = items

        # except:
        #     pass
        return data


def checkout(request):
    userprofile_object = UserProfile.objects.get(user=request.user)
    if not userprofile_object.phone:
        messages.info(
            request, f'Hi {request.user.username},  Please update your phone number in your profile to checkout')
        return redirect("core:order-summary")
    else:
        order = Order.objects.get(user=request.user, ordered=False)

        order_items = order.items.all()
        order_items.update(ordered=True)
        order.ordered = True
        order.save()

        for item in order_items:

            items = get_object_or_404(Item, pk=item.item.pk)
            items.sold += item.quantity
            items.save()

            item.save()
        user = request.user
        subject = 'AGMarket : Order Confirmation '
        message = f'Hi {user.username}, Thank you for your interest, We will get back to you soon.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        messages.info(
            request, f'Hi {request.user.username},  Your order has been checked out successfully. Check Your Email')

        return redirect("core:home")
    # context = {
    #     "items": Item.objects.all()
    # }

    # return render(request, "checkout-page.html", context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'main/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        items = Item.objects.all()
        category = categories.objects.all()
        data['categories'] = category
        data['items'] = items
        ImageFormSet = modelformset_factory(Images,
                                            form=ImageForm
                                            )

        if self.request.user.is_authenticated:
            pknew = self.request.user.id
            user_form = UserForm(instance=self.request.user)
            ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
                'phone', 'city', 'country', 'organization', 'photo',  'bio', ))
            # userformset = ProfileInlineFormset(instance=self.request.user)
            profile_id = UserProfile.objects.filter(user=request.user).first()
            userformset = UserProfileForm(instance=profile_id)
            

            postForm = AdditemForm()
            itemformset = ImageFormSet(queryset=Images.objects.none())
            data['noodle'] = pknew
            data['noodle_form'] = user_form
            data['userformset'] = userformset
            data['postForm'] = postForm
            data['formset'] = itemformset

        return data

# @ login_required
# def old_orders(request):
#     if request.method == 'GET':
#         order_item = OrderItem.objects.filter(user=request.user, ordered=True)
#         return render(request, 'main/old_detail.html', {'object': order_item, })

class old_orders_View(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order_item = OrderItem.objects.filter(user=self.request.user, ordered=True)

            context = {
                'object': order_item
            }
            return render(self.request, 'main/old_detail.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an any order")
            return redirect("/")


@ login_required
def addComment(request, pk):

    # if not request.user.has_perm('backend.change_artist'):
    #     raise PermissionDenied

    if request.method == 'POST':
        item = get_object_or_404(Item, pk=pk)
        user = request.user

        body = request.POST.get('body')
        sno = request.POST.get('commentsno')
        if sno == "":
            comment = Comment.objects.create(
                Item=item, body=body, user=user,)
            messages.info(request, "Your comment has been posted successfully")
        else:
            parent = get_object_or_404(Comment, sno=sno)
            comment = Comment.objects.create(
                Item=item, body=body, user=user, parent=parent)
            messages.info(request, "Your Reply has been posted successfully")

        return redirect("core:product", pk=pk)
    else:
        messages.info(request, "Your comment can not be published")
        return redirect("core:product", pk=pk)


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
 
    if item.user.id is request.user.id:
        messages.info(request, "You cannot add your own item to your cart.")
        return redirect("core:product", pk=pk)

    else:
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__pk=item.pk).exists():
                if order_item.quantity < order_item.item.available:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, "This item quantity was updated.")
                    return redirect("core:order-summary")
                else:

                    messages.info(request, "Out of Stock.")
                    return redirect("core:order-summary")
            else:
                order.items.add(order_item)
                messages.info(request, "सामान बास्केटमा राखियो ")
                return redirect("core:order-summary")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
        
        
@login_required
def place_item_bid(request,pk):
    item = get_object_or_404(Item, pk=pk)
 
    if item.user.id is request.user.id:
        messages.info(request, "You cannot place bid on your own item.")
        return redirect("core:product", pk=pk)
    else:
        item_bid = BidItem.objects.create(
            user_id=request.user.id,
            item_id = item.id,
            quantity= request.POST.get('quantity'),
            price=request.POST.get('price'))
        messages.info(request, "Your bid is successfully placed.")
        return redirect("core:product", pk=pk)


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", pk=pk)


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", pk=pk)


@ api_view(['GET', 'POST'])
@ login_required
def itemlist(request):
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm
                                        )

    if request.method == 'GET':
        category = categories.objects.all()
        items = Item.objects.all()

        postform = AdditemForm()
        postformset = ImageFormSet(queryset=Images.objects.none())
        pknew = request.user.id
        user_form = UserForm(instance=request.user)
        ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
            'phone', 'city', 'country', 'organization', 'photo',  'bio',))
        # userformset = ProfileInlineFormset(instance=request.user)
        profile_id = UserProfile.objects.filter(user=request.user).first()
        userformset = UserProfileForm(instance=profile_id)
        

        return render(request, "add_item.html", {'categories': category, 'items': items, 'postForm': postform, 'formset': postformset, "noodle": pknew,
                                                 "noodle_form": user_form,
                                                 "userformset": userformset, })

    elif request.method == 'POST':
        postForm = AdditemForm(request.POST, request.FILES)
        # formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())

        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            user = User.objects.get(pk=request.user.id)
            post_form.user_id = user.id
            mtest = post_form.save()
            iteminstance = Item.objects.get(pk=post_form.id)

            for img in request.FILES.getlist('form-0-image'):
                # print(item)
                Images.objects.get_or_create(item=iteminstance, image=img)

            messages.info(request, "Successfully posted your item")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors)


@login_required()  # only logged in users should access this
def edit_item(request, pk):
    item = Item.objects.get(pk=pk)
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm
                                        )
    if request.method == "GET":
        category = categories.objects.all()

        if request.user.is_authenticated:

            postform = AdditemForm(instance=item)
            postformset = ImageFormSet(queryset=Images.objects.none())
            item_images = Images.objects.filter(item=pk)
            pknew = request.user.id
            user_form = UserForm(instance=request.user)
            profile_id = UserProfile.objects.filter(user=request.user).first()
            userformset = UserProfileForm(instance=profile_id)

            return render(request, "add_item.html", {'categories': category, 'postForm': postform, 'formset': postformset, "noodle": pknew,
                                                     "noodle_form": user_form,"userformset": userformset,'item_images':item_images,'item':item })
        else:
            return render(request, "add_item.html", {'categories': category, })

    elif request.method == 'POST':
        postForm = AdditemForm(request.POST, request.FILES, instance=item)

        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            # user = get_object_or_404(User, pk=request.user.id)
            user = User.objects.get(pk=request.user.id)
            # print(user.id)

            post_form.user_id = user.id

            mtest = post_form.save()
            clear_all_images = request.POST.get('clear_all_images')
            clear_images = request.POST.getlist('clear_images')
            
            if(clear_all_images == 'on'):
                Images.objects.filter(item=item).delete()
            if len(clear_images) > 0:
                for img in clear_images:
                    print(clear_images,img)
                    Images.objects.get(pk=img).delete()
                        
            for img in request.FILES.getlist('form-0-image'):
                Images.objects.create(item=item, image=img)

            messages.info(request, "Successfully edited your item")
            return redirect('core:user_items',pk=request.user.id)
        else:
            print(postForm.errors, formset.errors)


@login_required()  # only logged in users should access this
def edit_user(request):

    if request.method == "POST":
        user_form = UserForm(instance=request.user)
        ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
            'phone', 'city', 'country', 'organization', 'photo',  'bio',))

        user = User.objects.get(pk=request.user.id)

        user_form = UserForm(request.POST, request.FILES, instance=user)
        

        formset = ProfileInlineFormset(
            request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            created_user = user_form.save(commit=False)
            formset = ProfileInlineFormset(
                request.POST, request.FILES, instance=created_user)

            if formset.is_valid():
                created_user.save()
                formset.save()
                messages.info(request, "Your profile  updated successfully")
                return HttpResponseRedirect("/")


@login_required()  # only logged in users should access this
def user_items(request, pk):
    # querying the User object with pk from url
    categoriestest = categories.objects.all()

    user = User.objects.get(pk=pk)
    items = Item.objects.filter(user=user)

    ImageFormSet = modelformset_factory(Images, form=ImageForm)
    postform = AdditemForm()
    postformset = ImageFormSet(queryset=Images.objects.none())

    pknew = request.user.id
    user_form = UserForm(instance=request.user)
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
        'phone', 'city', 'country', 'organization', 'photo',  'bio',))
    # userformset = ProfileInlineFormset(instance=request.user)
    profile_id = UserProfile.objects.filter(user=request.user).first()
    userformset = UserProfileForm(instance=profile_id)
    
    return render(request, "main/user_category_page.html", {'items': items, 'categories': categoriestest, 'noodle': pknew,
                                                            'noodle_form': user_form, 'userformset': userformset, 'postForm': postform, 'formset': postformset, })
@login_required()    
def user_items_bids(request,pk):
    
    user = User.objects.get(pk=pk)
    items = Item.objects.filter(user=user).values_list('id',flat=True)
    
    bid_items = BidItem.objects.filter(item__in=items,is_withdrawn=False)
    
    user_form = UserForm(instance=request.user)
    profile_id = UserProfile.objects.filter(user=request.user).first()
    userformset = UserProfileForm(instance=profile_id)
    
    return render(request, "main/item-bids.html",{'bid_items':bid_items,'noodle_form':user_form,'userformset':userformset})

@login_required()    
def withdraw_bid(request,pk):
    item = get_object_or_404(BidItem,pk=pk)
    bid_item = BidItem.objects.get(pk=pk,is_withdrawn=False)
    bid_item.is_withdrawn=True
    bid_item.save()
    
    return redirect("core:product", pk=item.item_id)
    

    # category = get_object_or_404(categories, pk=pk)
    # items = Item.objects.filter(category=category)
    # print("iam here ")

    # if request.user.is_authenticated:
    #     ImageFormSet = modelformset_factory(Images,
    #                                         form=ImageForm
    #                                         )
    #     postform = AdditemForm()
    #     postformset = ImageFormSet(queryset=Images.objects.none())
    #     pknew = request.user.id
    #     user_form = UserForm(instance=request.user)
    #     ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
    #         'phone', 'city', 'country', 'organization', 'photo',  'bio',))
    #     userformset = ProfileInlineFormset(instance=request.user)

    #     return render(request, "main/user_category_page.html", {'categories': category, 'items': items, 'postForm': postform, 'formset': postformset, "noodle": pknew,
    #                                                             "noodle_form": user_form,
    #                                                             "userformset": userformset, })
    # else:
    #     return render(request, "main/user_category_page.html", {'categories': category, 'items': items, })
