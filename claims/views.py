from django.http import JsonResponse
from .models import Claim
from registrations.dynamodb_helpers import get_claims_for_product

def create_claim(request, serial_number):
    if request.method == 'POST':
        claim = Claim(
            product=Product.objects.get(serial_number=serial_number),
            description=request.POST.get('description'),
            status='Pending'
        )
        claim.save()
        return JsonResponse({'status': 'Claim created successfully'})

def view_claims(request, serial_number):
    claims = get_claims_for_product(serial_number)
    return JsonResponse({'claims': claims})
