from django.db.models.signals import post_save
from django.dispatch import receiver
from api.screenplays.models import ScreenPlay  # Adjust the import path if needed

@receiver(post_save, sender=ScreenPlay)
def handle_screenplay_save(sender, instance, created, **kwargs):
    """
    This signal handler will be triggered after a screenplay is saved (updated or created).
    It will automatically update the scenes related to the screenplay.
    """
    # Call get_scenes on the screenplay instance when it's saved or updated
    # We can pass save=True to ensure the scenes are saved or updated in the DB
    instance.extract_scenes(save=True)
