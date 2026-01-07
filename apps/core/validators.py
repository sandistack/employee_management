import os
import re

from django.core.exceptions import ValidationError


def validate_image_file(file):
    """
    Validate image file for size and extension.
    Allowed extensions: .jpg, .jpeg, .png
    Max size: 5MB
    """
    # Max size 5MB
    if file.size > 5 * 1024 * 1024:
        raise ValidationError('File size cannot exceed 5MB')
    
    # Valid extensions
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError('Only JPG, JPEG, PNG allowed')


def validate_phone_number(value):
    """
    Validate phone number format.
    Must be 10-15 digits, start with '08' or '62'.
    """
    if not value:
        return
    
    # Remove non-numeric characters
    cleaned = re.sub(r'\D', '', value)
    
    # Check length
    if len(cleaned) < 10 or len(cleaned) > 15:
        raise ValidationError(
            'Nomor telepon harus 10-15 digit',
            code='invalid_length'
        )
    
    # Check prefix
    if not cleaned.startswith(('08', '62')):
        raise ValidationError(
            'Nomor telepon harus diawali 08 atau 62',
            code='invalid_prefix'
        )


def validate_email_domain(value):
    """
    Validate email format and block disposable email domains.
    Allowed disposable domains: tempmail.com, throwaway.email, 10minutemail.com, guerrillamail.com, mailinator.com, trashmail.com
    """
    if not value:
        return
    
    # Basic email format check (already handled by EmailField, but double check)
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError(
            'Format email tidak valid',
            code='invalid_format'
        )
    
    # Optional: Block disposable email domains
    disposable_domains = [
        'tempmail.com', 'throwaway.email', '10minutemail.com',
        'guerrillamail.com', 'mailinator.com', 'trashmail.com'
    ]
    
    domain = value.split('@')[1].lower()
    if domain in disposable_domains:
        raise ValidationError(
            'Email dari disposable domain tidak diperbolehkan',
            code='disposable_email'
        )
