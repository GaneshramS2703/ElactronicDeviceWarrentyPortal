from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from helpers.dynamodb_helpers import get_claims_for_product, put_item, delete_item
from registrations.models import Product

@login_required
def list_user_claims(request):
    """Displays all claims for the logged-in user's products."""
    try:
        # Fetch all products for the user
        products = Product.objects.filter(user=request.user)
        claims = []
        for product in products:
            product_claims = get_claims_for_product(product.serial_number)
            for claim in product_claims:
                claims.append({
                    'product_name': product.product_name,
                    **claim
                })
        return render(request, 'claims/list_claims.html', {'claims': claims})
    except Exception as e:
        messages.error(request, f"Error fetching claims: {e}")
        return render(request, 'claims/list_claims.html', {'claims': []})


@login_required
def create_claim(request, serial_number):
    """Handles the creation of a new claim for a specific product."""
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        if not description:
            messages.error(request, "Description is required.")
            return redirect('list_user_claims')
        try:
            put_item(
                user_id=request.user.id,
                serial_number=serial_number,
                description=description,
                status='Pending'
            )
            messages.success(request, "Claim created successfully.")
            return redirect('list_user_claims')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('list_user_claims')
    return render(request, 'claims/create_claim.html', {'serial_number': serial_number})


@login_required
def delete_claim(request, claim_id):
    """Handles deletion of a specific claim."""
    try:
        delete_item(request.user.id, claim_id)
        messages.success(request, "Claim deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting claim: {e}")
    return redirect('list_user_claims')
