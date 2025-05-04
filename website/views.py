import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .forms import RegistrationForm, ProductForm, VarietyForm, CategoryForm, CompanyForm, RegionForm, ProvinceForm, MunicipalityForm, BarangayForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile, Product, Variety, Category, Company, Product, Order, Cart, CartItem, Transaction, Receipt, OrderItem, TrackingLog, Region, Province, Municipality, Barangay
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Max, Q, Sum
from django.db import transaction
from django.db import transaction as db_transaction
from django.urls import reverse
from django.utils.timezone import now, timedelta
from uuid import uuid4

User = get_user_model()

def is_admin(user):
    return user.profile.user_type == 'admin'

def sales(request):
    return render (request, 'sales.html')

def Landingpage(request):
    return render (request, 'Landingpage.html')


@login_required
@user_passes_test(is_admin)
def manage_section(request):
    regions = Region.objects.all()
    provinces = Province.objects.all()
    municipalities = Municipality.objects.all()
    barangays = Barangay.objects.all()
    companies = Company.objects.all()
    users = User.objects.exclude(profile__user_type='admin').select_related('profile')
    user_groups = {
        'seller': users.filter(profile__user_type='seller'),
        'buyer': users.filter(profile__user_type='buyer'),
        'logistics': users.filter(profile__user_type='logistics'),
    }
    return render(request, 'Manage_section.html', {
        'companies': companies, 
        'user_groups': user_groups, 
        'regions': regions,
        'provinces': provinces, 
        'municipalities': municipalities,
        'barangays': barangays})


@login_required
@user_passes_test(is_admin)
def add_region(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')  # Success

        # ❗ If invalid, render the manage_locations page with the form errors
        regions = Region.objects.all()
        province_form = ProvinceForm()
        municipality_form = MunicipalityForm()
        barangay_form = BarangayForm()

        return render(request, 'manage_locations.html', {
            'region_form': form,
            'province_form': province_form,
            'municipality_form': municipality_form,
            'barangay_form': barangay_form,
            'regions': regions,
        })

    return redirect('manage_locations')

@login_required
@user_passes_test(is_admin)
def add_province(request):
    if request.method == 'POST':
        form = ProvinceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')  # Redirects to the manage locations page
    return redirect('manage_locations')

@login_required
@user_passes_test(is_admin)
def add_municipality(request):
    if request.method == 'POST':
        form = MunicipalityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')  # Redirects to the manage locations page
    return redirect('manage_locations')

@login_required
@user_passes_test(is_admin)
def add_barangay(request):
    if request.method == 'POST':
        form = BarangayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')  # Redirects to the manage locations page
    return redirect('manage_locations')

@login_required
@user_passes_test(is_admin)
def manage_locations(request):
    regions = Region.objects.all()
    provinces = Province.objects.select_related('region').all()
    municipalities = Municipality.objects.select_related('province').all()
    barangays = Barangay.objects.select_related('municipality').all()

    region_form = RegionForm()
    province_form = ProvinceForm()
    municipality_form = MunicipalityForm()
    barangay_form = BarangayForm()

    return render(request, 'manage_locations.html', {
        'regions': regions,
        'provinces': provinces,
        'municipalities': municipalities,
        'barangays': barangays,
        'region_form': region_form,
        'province_form': province_form,
        'municipality_form': municipality_form,
        'barangay_form': barangay_form
    })

@login_required
@user_passes_test(is_admin)
def edit_region(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    if request.method == 'POST':
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')
    else:
        form = RegionForm(instance=region)
    return render(request, 'edit_region.html', {'form': form, 'region': region})

@login_required
@user_passes_test(is_admin)
def edit_municipality(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    if request.method == 'POST':
        form = MunicipalityForm(request.POST, instance=municipality)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')
    else:
        form = MunicipalityForm(instance=municipality)
    return render(request, 'edit_municipality.html', {'form': form, 'municipality': municipality})

@login_required
@user_passes_test(is_admin)
def edit_barangay(request, barangay_id):
    barangay = get_object_or_404(Barangay, id=barangay_id)
    if request.method == 'POST':
        form = BarangayForm(request.POST, instance=barangay)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')
    else:
        form = BarangayForm(instance=barangay)
    return render(request, 'edit_barangay.html', {'form': form, 'barangay': barangay})

@login_required
@user_passes_test(is_admin)
def delete_region(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    region.delete()
    return redirect('manage_locations')

@login_required
@user_passes_test(is_admin)
def delete_province(request, province_id):
    province = get_object_or_404(Province, id=province_id)
    province.delete()
    return redirect('manage_locations')


@login_required
@user_passes_test(is_admin)
def delete_municipality(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    municipality.delete()
    return redirect('manage_locations')

@login_required
@user_passes_test(is_admin)
def delete_barangay(request, barangay_id):
    barangay = get_object_or_404(Barangay, id=barangay_id)
    barangay.delete()
    return redirect('manage_locations')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    regions = Region.objects.all()
    municipalities = Municipality.objects.all()
    barangays = Barangay.objects.all()
    companies = Company.objects.all()
    users = User.objects.exclude(profile__user_type='admin').select_related('profile')

    user_groups = {
        'seller': users.filter(profile__user_type='seller'),
        'buyer': users.filter(profile__user_type='buyer'),
        'logistics': users.filter(profile__user_type='logistics'),
    }

    # New counts
    seller_count = user_groups['seller'].count()
    buyer_count = user_groups['buyer'].count()
    logistics_count = user_groups['logistics'].count()
    company_count = companies.count()

    # For now, dummy 0 sales, unless you already have a sales model
    total_sales = Transaction.objects.aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'admin_dashboard.html', {
        'companies': companies,
        'user_groups': user_groups,
        'regions': regions,
        'municipalities': municipalities,
        'barangays': barangays,
        'seller_count': seller_count,
        'buyer_count': buyer_count,
        'logistics_count': logistics_count,
        'company_count': company_count,
        'total_sales': total_sales,
    })


#Adding Sections:
@login_required
@user_passes_test(is_admin)
def seller_section(request):    
    users = User.objects.exclude(profile__user_type='admin').select_related('profile')

    user_groups = {
        'seller': users.filter(profile__user_type='seller'),
        'buyer': users.filter(profile__user_type='buyer'),
        'logistics': users.filter(profile__user_type='logistics'),
    }

    return render(request, 'Seller_section.html', {'user_groups': user_groups,})

@login_required
@user_passes_test(is_admin)
def buyer_section(request):    
    users = User.objects.exclude(profile__user_type='admin').select_related('profile')

    user_groups = {
        'seller': users.filter(profile__user_type='seller'),
        'buyer': users.filter(profile__user_type='buyer'),
        'logistics': users.filter(profile__user_type='logistics'),
    }

    return render(request, 'Buyer_section.html', {'user_groups': user_groups,})

@login_required
@user_passes_test(is_admin)
def logistics_section(request):    
    users = User.objects.exclude(profile__user_type='admin').select_related('profile')

    user_groups = {
        'seller': users.filter(profile__user_type='seller'),
        'buyer': users.filter(profile__user_type='buyer'),
        'logistics': users.filter(profile__user_type='logistics'),
    }

    return render(request, 'Logistics_section.html', {'user_groups': user_groups,})

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def companies_section(request):
    """ View to manage companies and users. """
    regions = Region.objects.all()
    municipalities = Municipality.objects.all()
    barangays = Barangay.objects.all()
    companies = Company.objects.all()
    users = User.objects.exclude(profile__user_type='admin').select_related('profile')

    user_groups = {
        'seller': users.filter(profile__user_type='seller'),
        'buyer': users.filter(profile__user_type='buyer'),
        'logistics': users.filter(profile__user_type='logistics'),
    }

    return render(request, 'Companies_section.html', {
        'companies': companies,
        'user_groups': user_groups,
        'regions': regions,
        'municipalities': municipalities,
        'barangays': barangays
    })

def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.get(user=user)  
    return render(request, 'view_user.html', {'user': user, 'profile': profile})

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        profile.middle_name = request.POST.get('middle_name')
        profile.contact_number = request.POST.get('contact_number')
        profile.user_type = request.POST.get('user_type')
        profile.save()

        return redirect('admin_dashboard')

    return render(request, 'update_user.html', {'user': user, 'profile': profile})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    section = request.POST.get('section', 'admin_dashboard')  # Get from POST data

    if request.method == 'POST':
        user.delete()

    # Redirect based on section
    section_redirects = {
        'seller': 'seller_section',
        'buyer': 'buyer_section',
        'logistics': 'logistics_section',
    }

    return redirect(section_redirects.get(section, 'admin_dashboard'))

def login_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.profile.user_type == "admin":
                return redirect("admin_dashboard")  
            elif user.profile.user_type == "seller":
                return redirect("seller_dashboard")  
            elif user.profile.user_type == "buyer":
                return redirect("buyer_products")  
            elif user.profile.user_type == "logistics":
                return redirect("logistics_dashboard")  
            return redirect("home") 

        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html", {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('login')

def home_view(request):
    user = request.user

    # If the user is NOT logged in, redirect them to the login page
    if not user.is_authenticated:
        return render (request, 'Landingpage.html')

    # Redirect based on user type
    if hasattr(user, "profile"):  # Check if the user has a profile
        if user.profile.user_type == "admin":
            return redirect("admin_dashboard")
        elif user.profile.user_type == "seller":
            return redirect("seller_dashboard")
        elif user.profile.user_type == "buyer":
            return redirect("buyer_products")
        elif user.profile.user_type == "logistics":
            return redirect("logistics_dashboard")

    return redirect("login")  # Default fallback


def admin_view(request):
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'admin_dashboard.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Registration successful!'}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@user_passes_test(lambda u: u.profile.user_type == 'seller')
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()

            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Category added successfully!'})

            return redirect('seller_dashboard')

        # Return form errors for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})

    return redirect('seller_dashboard')  # Redirect for non-POST requests

@user_passes_test(lambda u: u.profile.user_type == 'seller')
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Product added successfully!'})

            return redirect('seller_dashboard')

        # Return form errors for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})

    return redirect('seller_dashboard') 

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.name = request.POST.get("productName")
        product.description = request.POST.get("productDescription")
        product.save()
        return redirect('seller_dashboard')  # Adjust this to your seller dashboard URL

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('seller_dashboard')  # Adjust this to your seller dashboard URL

@user_passes_test(lambda u: u.profile.user_type == 'seller')
@login_required
def add_variety(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        form = VarietyForm(request.POST)
        if form.is_valid():
            variety = form.save(commit=False)
            variety.product = product
            variety.save()

            # ✅ Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f"Variety added successfully to {product.name}."})

            # Standard redirect for non-AJAX requests
            messages.success(request, f"Variety added successfully to {product.name}.")
            return redirect('seller_dashboard')
        
        else:
            # ✅ Return form errors in JSON format for AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

            messages.error(request, "Failed to add variety. Please check the form.")
            return redirect('seller_dashboard')

    return JsonResponse({'success': False, 'message': "Invalid request method."}, status=400)

def edit_variety(request, variety_id):
    variety = get_object_or_404(Variety, id=variety_id)
    if request.method == "POST":
        variety.description = request.POST.get("description")
        variety.quantity = request.POST.get("quantity")
        variety.price = request.POST.get("price")
        variety.save()
        return redirect('seller_dashboard')  # Adjust the redirect URL as needed

def delete_variety(request, variety_id):
    variety = get_object_or_404(Variety, id=variety_id)
    if request.method == "POST":
        variety.delete()
        return redirect('seller_dashboard')  # Adjust the redirect URL as needed

@user_passes_test(lambda u: u.profile.user_type == 'seller')
@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user).prefetch_related('varieties')
    seller_orders = Order.objects.filter(order_items__product__seller=request.user, is_archived=False).distinct()
    logistics_users = User.objects.filter(profile__user_type='logistics')
    product_form = ProductForm()
    category_form = CategoryForm()  


    tracking_logs = TrackingLog.objects.filter(order__in=seller_orders).select_related('order', 'updated_by')

    return render(request, 'seller_dashboard.html', {
        'products': products,
        'seller_orders': seller_orders,
        'logistics_users': logistics_users,
        'tracking_logs': tracking_logs,
        'product_form': product_form, 
        'category_form': category_form,
        "variety_form": VarietyForm(),
    })

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            try:
                # Save the company with all form data, including the hierarchical location
                form.save()
                return redirect('admin_dashboard')  # Redirect to the admin dashboard on success
            except Exception as e:
                return render(request, 'add_company.html', {
                    'form': form,
                    'error': 'An unexpected error occurred. Please try again.'
                })

        return render(request, 'add_company.html', {
            'form': form,
            'error': 'Please correct the highlighted fields.'
        })

    # Render the form for GET requests
    form = CompanyForm()
    return render(request, 'add_company.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def view_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    users = User.objects.prefetch_related('profile').filter(profile__company=company)

    return render(request, 'view_company.html', {'company': company, 'users': users})

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def update_company(request, company_id):
    """ Handles updating a company via modal. """
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def delete_company(request, company_id):
    """ Handles deleting a company via modal. """
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        company.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
    
@login_required
@user_passes_test(lambda u: u.profile.user_type == 'buyer')
def available_products(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', 'all')

    buyer_company = request.user.profile.company  # Get buyer's company

    if buyer_company and buyer_company.municipality:
        # Filter products whose seller's company municipality matches the buyer's company municipality
        if selected_category == 'all':
            products = Product.objects.filter(
                is_available=True,
                seller__profile__company__municipality=buyer_company.municipality
            ).prefetch_related('varieties', 'category')
        else:
            products = Product.objects.filter(
                is_available=True,
                category__id=selected_category,
                seller__profile__company__municipality=buyer_company.municipality
            ).prefetch_related('varieties', 'category')
    else:
        # If buyer has no company or no municipality, show no products
        products = Product.objects.none()

    return render(request, 'buyer_products.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'buyer')
def order_tracking(request):
    # Get orders that are not archived or delivered
    active_orders = Order.objects.filter(
        buyer=request.user,
        is_archived=False,
    ).exclude(status="Delivered")

    # Get the latest tracking log for each active order
    latest_updates = (
        TrackingLog.objects.filter(order__in=active_orders)
        .values('order')  
        .annotate(latest_timestamp=Max('timestamp'))  # Get the latest timestamp per order
    )

    # Fetch the actual TrackingLog entries using the latest timestamps
    tracking_updates = TrackingLog.objects.filter(
        order__in=active_orders,
        timestamp__in=[entry["latest_timestamp"] for entry in latest_updates]  # Match only latest logs
    ).order_by("-timestamp")

    # Get corresponding receipt numbers for the orders
    for update in tracking_updates:
        transaction = Transaction.objects.filter(order=update.order).first()
        update.receipt_number = (
            transaction.receipt.receipt_number if transaction and hasattr(transaction, 'receipt') else "N/A"
        )
        update.transaction_id = transaction.id if transaction else None  

    return render(request, "My_orders.html", {"tracking_updates": tracking_updates})

# @login_required
# @user_passes_test(lambda u: u.profile.user_type == 'buyer')
# @transaction.atomic
# def purchase_variety(request, variety_id):
#     if request.method == 'POST':
#         variety = get_object_or_404(Variety, id=variety_id)
#         quantity = int(request.POST.get('quantity', 1))

#         if variety.quantity < quantity:
#             return JsonResponse({'status': 'error', 'message': 'Not enough stock available.'}, status=400)

#         variety.quantity -= quantity
#         variety.save()

#         Order.objects.create(
#             buyer=request.user,
#             product=variety.product,
#             variety=variety,
#             quantity=quantity,
#             total_price=variety.price * quantity
#         )

#         return JsonResponse({'status': 'success', 'message': 'Product purchased successfully!'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    
@login_required
@csrf_exempt
@user_passes_test(lambda u: u.profile.user_type == 'buyer')
def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            variety_id = data.get("variety_id")
            quantity = int(data.get("quantity"))

            if not variety_id or quantity < 1:
                return JsonResponse({"success": False, "message": "Invalid variety or quantity."})

            variety = get_object_or_404(Variety, id=variety_id)

            # Ensure quantity doesn't exceed available stock
            if quantity > variety.quantity:
                return JsonResponse({"success": False, "message": "Not enough stock available."})

            # Get or create the cart for the user
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Check if item already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, variety=variety)
            
            if not created:
                # If item exists, update quantity (but don't exceed stock)
                new_quantity = cart_item.quantity + quantity
                if new_quantity > variety.quantity:
                    return JsonResponse({"success": False, "message": "Exceeds available stock."})
                cart_item.quantity = new_quantity
            else:
                cart_item.quantity = quantity

            cart_item.save()

            return JsonResponse({"success": True, "message": "Item added to cart."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'buyer')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'buyer')
def remove_from_cart(request, cart_item_id):
    if request.method == "POST":
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            cart_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Item successfully removed from cart!'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found in your cart.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

from django.db import transaction
from django.http import JsonResponse

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'buyer')
@transaction.atomic
def checkout(request):
    cart = request.user.cart

    if not cart.items.exists():
        return JsonResponse({'status': 'error', 'message': 'Your cart is empty! Please add items before checking out.'})

    try:
        order = Order.objects.create(
            buyer=request.user,
            total_price=cart.total_price(),
            status="Pending"
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.variety.product,
                variety=item.variety,
                quantity=item.quantity,
                total_price=item.total_price()
            )
            item.variety.quantity -= item.quantity
            item.variety.save()

        TrackingLog.objects.create(
            order=order,
            status_update="Pending",
            updated_by=request.user
        )

        transaction = Transaction.objects.create(
            buyer=request.user,
            order=order,
            total_price=order.total_price
        )

        Receipt.objects.create(transaction=transaction)
        cart.items.all().delete()

        return JsonResponse({'status': 'success', 'message': 'Checkout successful! Redirecting to order tracking...'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})


@login_required
def receipt_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    order = transaction.order
    order_items = order.order_items.all()

    # Check if the user is the buyer
    is_buyer = request.user == transaction.buyer

    # Determine if the user can confirm delivery (status is "Arrived" and not archived)
    can_confirm_delivery = is_buyer and order.status == "Arrived" and not order.is_archived

    # Determine if the user can cancel the order (status is neither "Arrived" nor "Delivered")
    can_cancel_order = is_buyer and order.status not in ["Arrived", "Delivered"] and not order.is_archived

    if request.method == 'POST':
        if 'confirm_delivery' in request.POST and can_confirm_delivery:
            # Confirm delivery and archive the order
            order.status = "Delivered"
            order.is_archived = True
            order.save()

            TrackingLog.objects.create(
                order=order,
                updated_by=request.user,
                status_update="Delivered"
            )

            messages.success(request, "Delivery confirmed! Thank you for your purchase.")
            return redirect('transaction_history')

        if 'cancel_order' in request.POST and can_cancel_order:
            # Cancel the order and archive it
            order.status = "Cancelled"
            order.is_archived = True
            order.save()

            TrackingLog.objects.create(
                order=order,
                updated_by=request.user,
                status_update="Cancelled"
            )

            messages.success(request, "Your order has been successfully cancelled.")
            return redirect('transaction_history')

    return render(request, 'receipt.html', {
        'transaction': transaction,
        'order': order,
        'order_items': order_items,
        'can_confirm_delivery': can_confirm_delivery,
        'can_cancel_order': can_cancel_order,
    })

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'buyer')
def transaction_history(request):
    transactions = (
        Transaction.objects.filter(
            buyer=request.user,
            order__status__in=["Delivered", "Cancelled"]
        )
        .select_related("receipt", "order")  # Include related order for tracking history
        .order_by("-created_at")
    )

    return render(request, "transaction_history.html", {"transactions": transactions})

@login_required
def claim_order(request, order_id):
    """ Logistics user claims an order for delivery """
    user = request.user

    if user.profile.user_type != "logistics":
        messages.error(request, "You are not authorized to claim orders.")
        return redirect("logistics_dashboard")

    order = get_object_or_404(Order, id=order_id)

    if order.claimed_by:
        messages.error(request, "This order has already been claimed.")
        return redirect("logistics_dashboard")

    # Ensure the logistics user is within the seller's municipality
    first_item = order.order_items.first()
    if not first_item:
        messages.error(request, "Invalid order. No associated products.")
        return redirect("logistics_dashboard")

    seller_municipality = first_item.product.seller.profile.company.municipality
    logistics_municipality = user.profile.company.municipality

    if seller_municipality != logistics_municipality:
        messages.error(request, "You can only claim orders within your municipality.")
        return redirect("logistics_dashboard")

    # Assign the order
    order.claimed_by = user
    order.claimed_at = now()
    order.save()

    # Log the tracking update
    TrackingLog.objects.create(
        order=order,
        logistics_user=user,
        status_update=f"Order claimed by {user.username}",
        updated_by=user
    )

    messages.success(request, f"You have claimed Order {order.id}.")
    return redirect("logistics_dashboard")

@user_passes_test(lambda u: u.profile.user_type == 'seller')
@login_required
def seller_tracking(request):
    seller_orders = Order.objects.filter(order_items__product__seller=request.user).distinct()
    logistics_users = User.objects.filter(profile__user_type='logistics')

    # Fetch the latest tracking logs
    latest_tracking_logs = (
        TrackingLog.objects
        .filter(order__order_items__product__seller=request.user)
        .values('order_id')
        .annotate(latest_timestamp=Max('timestamp'))
    )

    tracking_logs = TrackingLog.objects.filter(
        order_id__in=[log['order_id'] for log in latest_tracking_logs],
        timestamp__in=[log['latest_timestamp'] for log in latest_tracking_logs]
    ).exclude(status_update="Delivered")

    # Get transactions linked to seller orders
    transactions = Transaction.objects.filter(order__in=seller_orders).select_related('receipt')

    return render(request, 'seller_tracking.html', {
        'seller_orders': seller_orders,
        'logistics_users': logistics_users,
        'tracking_logs': tracking_logs,
        'transactions': transactions,
    })

def reassign_unclaimed_orders():
    """ Check for unclaimed orders and reassign them when necessary """
    unclaimed_orders = Order.objects.filter(
        status="Pending",
        claimed_by__isnull=True,
        claimed_at__lte=now() - timedelta(hours=1)  # Orders unclaimed for over an hour
    )

    for order in unclaimed_orders:
        seller_municipality = order.order_items.first().product.seller.profile.company.municipality

        # Get the next available logistics user in the same municipality, excluding previous assignees
        available_logistics = Profile.objects.filter(
            user_type="logistics",
            company__municipality=seller_municipality
        ).exclude(user=order.claimed_by).order_by("?")  # Randomly pick next user

        if available_logistics.exists():
            new_logistics = available_logistics.first().user
            order.claimed_by = new_logistics
            order.claimed_at = now()
            order.save()

            TrackingLog.objects.create(
                order=order,
                logistics_user=new_logistics,
                status_update=f"Reassigned to {new_logistics.username}",
                updated_by=None
            )

@login_required
def logistics_dashboard(request):
    """ Dashboard for logistics users - checks for orders to claim and handles rotation """
    user = request.user

    if user.profile.user_type != "logistics":
        return redirect("home")  # Redirect unauthorized users

    # Call the reassignment function when logistics users access the dashboard
    reassign_unclaimed_orders()

    # Get available transactions within user's municipality
    available_transactions = Transaction.objects.filter(
        order__status="Pending",
        order__claimed_by__isnull=True,
        order__order_items__product__seller__profile__company__municipality=user.profile.company.municipality
    ).distinct().select_related("order__buyer").prefetch_related("order__tracking_logs")

    # Get the logistics user's claimed transactions, excluding Delivered and Archived
    my_transactions = Transaction.objects.filter(
        order__claimed_by=user
    ).exclude(
        order__status__in=["Delivered", "Archived", "Cancelled"]
    ).distinct().select_related("order__buyer").prefetch_related("order__tracking_logs", "receipt")

    return render(request, "logistics_dashboard.html", {
        "available_transactions": available_transactions,
        "my_transactions": my_transactions,
    })

@login_required
def update_tracking_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = request.user

    # Ensure authorized access
    if order.claimed_by != user and user.profile.user_type not in ['logistics', 'buyer']:
        return HttpResponseForbidden("You are not authorized to update this order.")

    order_items = order.order_items.all()
    picked_up_items = order_items.filter(is_picked_up=True).count()
    total_items = order_items.count()

    # Prevent modifications to archived orders
    if order.is_archived:
        messages.error(request, "This order has been completed and archived. No further updates can be made.")
        return redirect('logistics_dashboard')

    if request.method == 'POST':
        new_status = request.POST.get('status_update')

        if user.profile.user_type == 'logistics':
            # Step 1: Marking items as picked up
            if new_status == 'Picked Up':
                item_id = request.POST.get('item_id')
                item = get_object_or_404(OrderItem, id=item_id, order=order)

                if item.is_picked_up:
                    messages.error(request, "This item has already been picked up.")
                else:
                    item.is_picked_up = True
                    item.save()
                    messages.success(request, f"Item '{item.product.name}' marked as picked up.")

                # If all items are picked up, update order to 'Shipped'
                picked_up_items = order.order_items.filter(is_picked_up=True).count()
                if picked_up_items == total_items:
                    order.status = "Shipped"
                    order.save()
                    TrackingLog.objects.create(order=order, updated_by=user, status_update="Shipped")

            # Step 2: Marking In Transit
            elif new_status == 'In Transit' and order.status == "Shipped":
                order.status = "In Transit"
                order.save()
                TrackingLog.objects.create(order=order, updated_by=user, status_update="In Transit")
                messages.success(request, f"Order {order.id} is now In Transit.")

            # Step 3: Marking Arrived
            elif new_status == 'Arrived' and order.status == "In Transit":
                order.status = "Arrived"
                order.save()
                TrackingLog.objects.create(order=order, updated_by=user, status_update="Arrived")
                messages.success(request, f"Order {order.id} has arrived at the delivery location.")

        elif user.profile.user_type == 'buyer':
            # Step 4: Confirming Delivery
            if new_status == 'Delivered' and order.status == "Arrived":
                order.status = "Delivered"
                order.is_archived = True
                order.save()
                TrackingLog.objects.create(order=order, updated_by=user, status_update="Delivered")
                messages.success(request, f"Order {order.id} has been marked as Delivered.")

        return redirect('logistics_dashboard')

    context = {
        'order': order,
        'order_items': order_items,
        'picked_up_items': picked_up_items,
        'total_items': total_items,
    }

    return render(request, 'update_tracking_status.html', context)


from django.db.models import Q

@login_required
def archived_orders(request):
    if request.user.profile.user_type == 'seller':
        # Seller sees only their delivered or canceled orders
        archived_orders = Order.objects.filter(
            order_items__product__seller=request.user,
            is_archived=True,
            status__in=["Delivered", "Cancelled"]
        ).distinct()

    elif request.user.profile.user_type == 'logistics':
        # Logistics see archived orders they claimed or were associated with during cancellation
        archived_orders = Order.objects.filter(
            is_archived=True,
            status__in=["Delivered", "Cancelled"]
        ).filter(
            Q(claimed_by=request.user) | 
            Q(tracking_logs__updated_by=request.user)  # Associated by tracking updates (logistics interactions)
        ).distinct()

    elif request.user.profile.user_type == 'buyer':
        # Buyers see their delivered or canceled orders
        archived_orders = Order.objects.filter(
            buyer=request.user,
            is_archived=True,
            status__in=["Delivered", "Cancelled"]
        )

    else:
        return HttpResponseForbidden("You are not authorized to view this page.")

    transactions = Transaction.objects.filter(order__in=archived_orders)
    receipts = Receipt.objects.filter(transaction__in=transactions)

    return render(request, 'archived_orders.html', {
        'archived_orders': archived_orders,
        'transactions': transactions,
        'receipts': receipts
    })

@login_required
def tracking_history(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    tracking_logs = order.tracking_logs.all()

    transaction = order.transactions.first()  # Get the first transaction linked to the order
    receipt_number = transaction.receipt.receipt_number if transaction and transaction.receipt else None

    return render(request, 'tracking_history.html', {
        'order': order,
        'tracking_logs': tracking_logs,
        'receipt_number': receipt_number,
    })

def profile(request):
    user = request.user  
    profile, created = Profile.objects.get_or_create(user=user)  # Ensure Profile exists

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()  # Save User model changes

            profile.save()  # Save Profile changes
            return redirect('profile')  # Redirect back to profile page after update
    else:
        # Pre-fill the form with existing data
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })

    return render(request, 'profile.html', {'form': form})

@login_required
def change_password(request):
    """Allow users to change their password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout
            messages.success(request, "Your password was successfully updated!")
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

@login_required
def delete_account(request):
    """Allow users to delete their account."""
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')

    return render(request, 'confirm_delete_account.html')

def get_provinces(request, region_id):
    provinces = Province.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(provinces), safe=False)

def get_municipalities(request, province_id):
    municipalities = Municipality.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(municipalities), safe=False)

def get_barangays(request, municipality_id):
    barangays = Barangay.objects.filter(municipality_id=municipality_id).values('id', 'name')
    return JsonResponse(list(barangays), safe=False)
