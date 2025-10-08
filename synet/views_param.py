# synet/views_param.py
from django.http import JsonResponse
from .models import Parametroi

def get_collector_fee_rate(request):
    """
    Επιστρέφει το ποσοστό εισπράκτορα (collectorFeeRate) από τον πίνακα parametroi
    ώστε να μπορεί να χρησιμοποιηθεί δυναμικά από React ή Ajax.
    """
    try:
        rate_obj = Parametroi.objects.get(param="collectorFeeRate")
        rate = float(rate_obj.value)
    except (Parametroi.DoesNotExist, ValueError):
        rate = 0.06  # default αν λείπει

    return JsonResponse({"collectorFeeRate": rate})
