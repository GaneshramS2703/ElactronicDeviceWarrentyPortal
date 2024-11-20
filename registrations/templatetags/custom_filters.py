from django import template
from helpers.s3_helpers import generate_presigned_url

register = template.Library()

@register.filter
def generate_presigned_url_filter(file_key):
    """Generate a presigned URL for the given S3 file key."""
    return generate_presigned_url(file_key)
print("Debug: Custom filter library loaded.")
