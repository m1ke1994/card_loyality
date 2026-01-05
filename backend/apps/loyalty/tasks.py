from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import ActiveVisit, Visit


@shared_task
def auto_close_active_visits():
    cutoff = timezone.now() - timedelta(hours=settings.ACTIVE_VISIT_AUTO_CLOSE_HOURS)
    stale = ActiveVisit.objects.filter(last_activity_at__lt=cutoff, status="locked")
    for active in stale:
        Visit.objects.create(
            tenant=active.tenant,
            user=active.user,
            place=active.place,
            started_at=active.started_at,
            ended_at=timezone.now(),
            status="closed",
            points_earned=0,
            points_spent=0,
        )
        active.status = "closed"
        active.save(update_fields=["status"])
