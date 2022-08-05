from celery import shared_task


@shared_task(name="auto_bind")
def auto_bind():
    pass
