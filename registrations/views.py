from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def create_product(request):
    """Handles the creation of a new product."""
    if request.method == 'POST':
        try:
            product = Product.objects.create(
                user=request.user,
                serial_number=request.POST.get('serial_number'),
                product_name=request.POST.get('product_name'),
                purchase_date=request.POST.get('purchase_date'),
                warranty_period=request.POST.get('warranty_period'),
                description=request.POST.get('description', ''),
            )
            product.save()
            return HttpResponseRedirect(reverse('list_products'))
        except Exception as e:
            return render(request, 'registrations/create_product.html', {'error': str(e)})

    return render(request, 'registrations/create_product.html')


@login_required
def view_product(request, serial_number):
    """Displays details of a specific product."""
    product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
    return render(request, 'registrations/view_product.html', {'product': product})


@login_required
def list_products(request):
    """Lists all products registered by the logged-in user."""
    products = Product.objects.filter(user=request.user)
    return render(request, 'registrations/list_products.html', {'products': products})


@login_required
def delete_product_confirmation(request, serial_number):
    """Displays a confirmation page before deleting a product."""
    product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
    return render(request, 'registrations/delete_product_confirmation.html', {'product': product})


@login_required
def delete_product(request, serial_number):
    """Handles deletion of a specific product."""
    product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('list_products'))
    return render(request, 'registrations/delete_product_confirmation.html', {'product': product})
