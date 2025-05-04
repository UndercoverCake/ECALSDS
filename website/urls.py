from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('sales/', views.sales, name='sales'),    
    path('Landingpage/', views.Landingpage, name='Landingpage'),

    # Authentication
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Admin Dashboard & User Management
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/<int:user_id>/view/', views.view_user, name='view_user'),
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('sellers/', views.seller_section, name='seller_section'),
    path('buyers/', views.buyer_section, name='buyer_section'),
    path('logistics/', views.logistics_section, name='logistics_section'),
    path('companies/', views.companies_section, name='company_section'),
    path('locations/', views.manage_locations, name='manage_locations'),

    # Seller Dashboard & Product Management
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('category/add/', views.add_category, name='add_category'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/add-variety/', views.add_variety, name='add_variety'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-variety/<int:variety_id>/', views.edit_variety, name='edit_variety'),
    path('delete-variety/<int:variety_id>/', views.delete_variety, name='delete_variety'),

    # Buyer-related Paths
    path('buyer/products/', views.available_products, name='buyer_products'),
    path('products/', views.available_products, name='available_products'),
    path('buyer/cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('buyer/cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buyer/cart/checkout/', views.checkout, name='checkout'),
    # path('buyer/purchase/<int:variety_id>/', views.purchase_variety, name='purchase_variety'),

    # Order, Tracking & Transactions
    path('order/<int:order_id>/tracking/', views.tracking_history, name='tracking_history'),
    path('seller-tracking/', views.seller_tracking, name='seller_tracking'),
    #path('assign-logistics/<int:order_id>/', views.assign_logistics, name='assign_logistics'),
    path('order/<int:order_id>/update-tracking/', views.update_tracking_status, name='update_tracking_status'),
    path('orders/', views.order_tracking, name='order_tracking'),
    path('archived-orders/', views.archived_orders, name='archived_orders'),

    # Logistics Dashboard
    path('logistics-dashboard/', views.logistics_dashboard, name='logistics_dashboard'),
    path("dashboard/", views.logistics_dashboard, name="logistics_dashboard"),
    path("claim_order/<int:order_id>/", views.claim_order, name="claim_order"),


    # Transaction & Receipt Management
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('receipt/<int:transaction_id>/', views.receipt_view, name='receipt_view'),

    # Company Management
    path('company/add-company', views.add_company, name='add_company'),
    path('company/<int:company_id>/view/', views.view_company, name='view_company'),
    path('company/<int:company_id>/update/', views.update_company, name='update_company'),
    path('company/<int:company_id>/delete/', views.delete_company, name='delete_company'),

    # Location Management (Regions, Municipalities, Barangays)
    path('manage-section/', views.manage_section, name='manage_section'),
    path('add-region/', views.add_region, name='add_region'),
    path('add-province/', views.add_province, name='add_province'),
    path('add-municipality/', views.add_municipality, name='add_municipality'),
    path('add-barangay/', views.add_barangay, name='add_barangay'),
    path('manage-locations/', views.manage_locations, name='manage_locations'),
    path('locations/region/<int:region_id>/edit/', views.edit_region, name='edit_region'),
    path('locations/municipality/<int:municipality_id>/edit/', views.edit_municipality, name='edit_municipality'),
    path('locations/barangay/<int:barangay_id>/edit/', views.edit_barangay, name='edit_barangay'),
    path('locations/region/<int:region_id>/delete/', views.delete_region, name='delete_region'),
    path('locations/municipality/<int:municipality_id>/delete/', views.delete_municipality, name='delete_municipality'),
    path('locations/barangay/<int:barangay_id>/delete/', views.delete_barangay, name='delete_barangay'),

    # User profile management
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),

    #Locations
    path('get-provinces/<int:region_id>/', views.get_provinces, name='get_provinces'),
    path('get-municipalities/<int:province_id>/', views.get_municipalities, name='get_municipalities'),
    path('get-barangays/<int:municipality_id>/', views.get_barangays, name='get_barangays'),

    # path('pick-up/<int:order_id>/<int:item_id>/', views.pick_up_item, name='pick_up_item'),
    # path('in-transit/<int:order_id>/', views.mark_in_transit, name='mark_in_transit'),
    # path('arrived/<int:order_id>/', views.mark_arrived, name='mark_arrived'),
    # path('delivered/<int:order_id>/', views.mark_delivered, name='mark_delivered'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

