import os
from django.core.exceptions import ValidationError

def validate_is_zip(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in ['.zip']:
        raise ValidationError('zipファイルのみ許可されています')