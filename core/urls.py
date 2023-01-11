from django.urls import path
from .views import *
from django.conf.urls import url

app_name = 'core'

urlpatterns = [
    path('', HomeView, name='home'),
    
    path('accounts/update/<int:pk>/',updateUserProfile , name='account_update'),
    

    path('product/<int:pk>/', ItemDetailView.as_view(), name='product'),
    path('product/<int:pk>/withdraw-bid', withdraw_bid, name='withdraw_bid'),
    path('category/<int:pk>/', categoryview, name='category'),


    path('checkout/', checkout, name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),

    path('old-orders/', old_orders_View.as_view(), name='old-orders'),

    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    
    path('place-item-bid/<int:pk>/', place_item_bid, name='place-item-bid'),
    path('about/', about, name='about'),
    path('terms/', terms, name='terms'),


    path('add-item/', itemlist, name='add_item'),
    path('subscribe/', subscribe, name='subscribe'),

    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<int:pk>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('product/<int:pk>/comment', addComment, name='add_comment'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('accounts/update/', edit_user, name='account_update'),

    url(r'^users/items/(?P<pk>[\-\w]+)/$',
        user_items, name='user_items'),
    url(r'^users/items-bid/(?P<pk>[\-\w]+)/$',
        user_items_bids, name='user_items_bids'),
    url(r'^edit/item/(?P<pk>[\-\w]+)/$',
        edit_item, name='edit_item'),
    path('item-like/<int:pk>', ItemLike, name="item_like"),








]
