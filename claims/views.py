from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from helpers.dynamodb_helpers import get_claims_for_product, put_item, delete_item, get_user_products
from registrations.models import Product
from uuid import uuid4
from helpers.dynamodb_helpers import delete_item

@login_required
def list_user_claims(request):
    """Displays all claims for the logged-in user's products."""
    try:
        # Retrieve products for the logged-in user
        products = get_user_products(user_id=request.user.id)
        all_claims = []

        # Iterate through each product and retrieve its claims
        for product in products:
            claims = get_claims_for_product(product['SK'][8:])  # Extract serial number
            for claim in claims:
                # Ensure keys are accessed with correct case-sensitive names
                all_claims.append({
                    'product_serial': product['SK'][8:],  # Remove "PRODUCT#" prefix
                    'product_name': product['ProductName'],
                    'claim_id': claim['SK'].split('#')[1],  # Extract claim ID
                    'description': claim.get('Description', 'No description provided'),
                    'status': claim.get('status', 'pending'),  # Default to 'Pending' if not set
                })

        # Render the claims list page with the retrieved claims
        return render(request, 'claims/list_claims.html', {'claims': all_claims, 'products': products})
    except Exception as e:
        # Handle any exceptions and render the error
        return render(request, 'claims/list_claims.html', {'error': str(e)})



@login_required
def create_claim(request, serial_number):
    """Handles the creation of a new claim for a specific product."""
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        if not description:
            messages.error(request, "Description is required.")
            return redirect('create_claim', serial_number=serial_number)

        try:
            # Generate a unique claim ID
            claim_id = str(uuid4())[:8]  # Shorten UUID for simplicity

            # Save the claim to DynamoDB
            put_item(
                PK=f"PRODUCT#{serial_number}",
                SK=f"CLAIM#{claim_id}",
                description=description,
                status='Pending'
            )

            # Success message and redirect
            messages.success(request, "Claim created successfully.")
            return redirect('list_user_claims')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('create_claim', serial_number=serial_number)

    return render(request, 'claims/create_claim.html', {'serial_number': serial_number})


@login_required
def delete_claim(request, claim_id):
    """Delete a specific claim."""
    try:
        serial_number = request.GET.get('serial_number')
        if not serial_number:
            raise ValueError("Serial number is required to delete a claim.")

        PK = f"PRODUCT#{serial_number}"
        SK = f"CLAIM#{claim_id}"

        delete_item(PK=PK, SK=SK)
        messages.success(request, "Claim deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('list_user_claims')

@login_required
def view_claims(request, serial_number):
    """Displays all claims for a specific product."""
    try:
        product = get_object_or_404(Product, serial_number=serial_number, user=request.user)
        claims = get_claims_for_product(serial_number)
        return render(request, 'claims/view_claims.html', {'product': product, 'claims': claims})
    except Exception as e:
        messages.error(request, f"Error fetching claims: {e}")
        return redirect('list_user_claims')
