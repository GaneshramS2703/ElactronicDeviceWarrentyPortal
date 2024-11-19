from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Claim
from registrations.models import Product
from registrations.dynamodb_helpers import get_claims_for_product

@login_required
def create_claim(request, serial_number):
    """Handles the creation of a new claim for a specific product."""
    product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
    if request.method == 'POST':
        try:
            description = request.POST.get('description', '').strip()
            if not description:
                return render(request, 'claims/create_claim.html', {'product': product, 'error': 'Description is required'})

            claim = Claim.objects.create(
                product=product,
                description=description,
                status='Pending'
            )
            claim.save()
            return HttpResponseRedirect(reverse('view_claims', args=[serial_number]))
        except Exception as e:
            return render(request, 'claims/create_claim.html', {'product': product, 'error': str(e)})

    return render(request, 'claims/create_claim.html', {'product': product})


@login_required
def view_claims(request, serial_number):
    """Displays all claims for a specific product."""
    product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
    claims = get_claims_for_product(serial_number)
    return render(request, 'claims/view_claims.html', {'product': product, 'claims': claims})


@login_required
def list_user_claims(request):
    """Displays all claims across all products owned by the logged-in user."""
    try:
        products = Product.objects.filter(user=request.user)
        all_claims = []
        for product in products:
            claims = get_claims_for_product(product.serial_number)
            for claim in claims:
                all_claims.append({
                    'product_serial': product.serial_number,
                    'product_name': product.product_name,
                    **claim
                })
        return render(request, 'claims/list_claims.html', {'claims': all_claims})
    except Exception as e:
        return render(request, 'claims/list_claims.html', {'error': str(e)})


@login_required
def delete_claim_confirmation(request, claim_id):
    """Displays a confirmation page before deleting a claim."""
    claim = get_object_or_404(Claim, id=claim_id, product__user=request.user)
    return render(request, 'claims/delete_claim_confirmation.html', {'claim': claim})


@login_required
def delete_claim(request, claim_id):
    """Handles deletion of a specific claim."""
    claim = get_object_or_404(Claim, id=claim_id, product__user=request.user)
    if request.method == 'POST':
        claim.delete()
        return HttpResponseRedirect(reverse('list_user_claims'))
    return render(request, 'claims/delete_claim_confirmation.html', {'claim': claim})
