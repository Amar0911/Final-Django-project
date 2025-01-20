from .models import UserSubscription

def subscription_status(request):
    """
    Add `has_active_subscription` to the context for all templates.
    """
    if request.user.is_authenticated:
        has_active_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).exists()
    else:
        has_active_subscription = False

    return {
        'has_active_subscription': has_active_subscription,
    }
