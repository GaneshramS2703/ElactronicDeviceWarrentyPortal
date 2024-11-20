from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product
from helpers.dynamodb_helpers import get_item, put_item
from django.contrib import messages
from helpers.dynamodb_helpers import save_product
from django.shortcuts import render, redirect
from helpers.dynamodb_helpers import get_user_products
from helpers.dynamodb_helpers import delete_product_dynamodb


@login_required
def create_product(request):
    """Handles the creation of a new product."""
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number').strip()
        product_name = request.POST.get('product_name').strip()
        purchase_date = request.POST.get('purchase_date').strip()
        warranty_period = request.POST.get('warranty_period').strip()

        if not serial_number or not product_name or not purchase_date or not warranty_period:
            messages.error(request, "All fields are required.")
            return render(request, 'registrations/create_product.html')

        try:
            save_product(
                user_id=request.user.id,
                serial_number=serial_number,
                product_name=product_name,
                purchase_date=purchase_date,
                warranty_period=int(warranty_period)
            )
            messages.success(request, "Product registered successfully.")
            return redirect('list_products')  # Redirect to the product list page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'registrations/create_product.html')

    return render(request, 'registrations/create_product.html')

@login_required
def view_product(request, serial_number):
    """Displays details of a specific product."""
    product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
    return render(request, 'registrations/view_product.html', {'product': product})


@login_required
def list_products(request):
    """Displays all products registered by the logged-in user."""
    try:
        # Fetch products for the logged-in user
        products = get_user_products(user_id=request.user.id)
        return render(request, 'registrations/list_products.html', {'products': products})
    except Exception as e:
        return render(request, 'registrations/list_products.html', {'error': str(e)})




@login_required
def delete_product(request, serial_number):
    """Directly deletes a product without confirmation."""
    try:
        # Delete the product using the helper function
        delete_product_dynamodb(user_id=request.user.id, serial_number=serial_number)
        messages.success(request, "Product deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the product: {str(e)}")
    
    # Redirect to the product list page after deletion
    return redirect('list_products')
    
    
@login_required
def delete_product_confirmation(request, serial_number):
    """Displays a confirmation page before deleting a product."""
    from helpers.dynamodb_helpers import get_product
    print(f"Debug: Trying to fetch product USER#{request.user.id}, PRODUCT#{serial_number}")
    product = get_product(user_id=request.user.id, serial_number=serial_number)

    if not product:
        messages.error(request, "Product not found.")
        return redirect('list_products')  # Redirect to the product list if not found

    return render(request, 'registrations/delete_product_confirmation.html', {'product': product})


