from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from core.models import WordLevel, Review


@login_required
def dashboard(request):
    now = timezone.now()
    discovery_queue_size = WordLevel.objects.filter(user_id=request.user.id).filter(level=0).count()
    review_queue_size = Review.objects.filter(user_id=request.user.id).filter(date__lt=now).count()
    return render(
        request,
        'dashboard.html',
        {
            'discovery_queue_size': discovery_queue_size,
            'review_queue_size': review_queue_size
        }
    )
