from email.policy import default
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=("Profile Picture"),
                              upload_to=("profile_photos/"), null=True, blank=True)

    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)

    def create_profile(sender, **kwargs):

        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = UserProfile(
                user=user, bio='my bio')
            user_profile.save()
    post_save.connect(create_profile, sender=User)

    def __str__(self):
        return self.user.username


class categories(models.Model):
    category = models.CharField(max_length=100, unique=True)
    category_ne = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.category}"

    def get_absolute_url(self):
        return reverse("core:category", kwargs={"pk": self.pk})
    
    
def convertToNepali(input):
    return str(input).replace(',',',').replace('.','.').replace('0','०').replace('1','१').replace('2','२').replace('3','३').replace('4','४').replace('5','५').replace('6','६').replace('7','७').replace('8','८').replace('9','९')

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        categories, to_field='category', on_delete=models.CASCADE, null=True)

    # pk = models.pkField()
    available = models.IntegerField(default=1)
    sold = models.IntegerField(default=0)
    unit = models.CharField(max_length=10, default="Kg")
    home_delivery = models.BooleanField(default=False)
    show_expiry = models.BooleanField(default=False)
    price_negotiable = models.BooleanField(default=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images/', default=None)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    expiry_date = models.DateField(null=True,blank=True)
    upload_date = models.DateField(auto_now_add=True, null=True)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User, related_name='item_like',  blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def get_available_item(self):
        available_quantity = self.available-self.sold
        if(available_quantity < 1):
            return 'Out of Stock'
        else:
            return '%s  %s' % (self.available-self.sold, self.unit)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'pk': self.pk
        })
    def get_place_bid_url(self):
        return reverse("core:place-item-bid", kwargs={
            'pk': self.pk
        })

    def get_add_comment_url(self):
        return reverse("core:add_comment", kwargs={
            'pk': self.pk
        })

    def get_like_url(self):
        return reverse("core:item_like", kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'pk': self.pk
        })

    def get_add_itemurl(self):
        return reverse("core:add_item", kwargs={
            'user': self.user
        })

    def get_remaining_days(self):

        return (self.expiry_date-self.upload_date)

    def get_discount_percent(self):
        try:
            percent = (self.price-self.discount_price)/self.price*100

            return round(percent, 2)
        except:
            return 0

def get_image_filename(instance, filename):
    try:

        id = instance.item.id
        return "item_images/%s/%s" % (id,filename)
    except:
        return "item_images/"


class Images(models.Model):
    item = models.ForeignKey(Item, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image', default=None)

    def __str__(self):
        return self.item.title


class advertisement(models.Model):
    PLACEMENT_CHOICES = (
        ('ad1', 'Near slider'),
        ('ad2', 'After 6 post'),
        ('ad3', 'Before top product'),

    )
    image = models.ImageField()
    placement = models.CharField(choices=PLACEMENT_CHOICES, max_length=10)
    expiry_date = models.DateField(null=True)
    upload_date = models.DateField(auto_now_add=True, null=True)

    def get_remaining_days(self):

        return (self.expiry_date-self.upload_date)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class BidItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    bid_date = models.DateTimeField(auto_now_add=True, null=True)
    is_withdrawn = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    

class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    Item = models.ForeignKey(
        Item, related_name="comments", on_delete=models.CASCADE)

    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s - %s -%s' % (self.Item.title, self.user.username, self.body)

    def __unicode__(self):
        return


class aboutpage(models.Model):
    Content = models.TextField()


class subscripiton(models.Model):
    email = models.EmailField()
