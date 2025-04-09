from api.authentication.services import signup
from api.users.enums import SetUpStatus
from api.users.models import User

SETUP_STATUS_ADAPTER = {
    signup.SetUpStatus.VALIDATED: SetUpStatus.VALIDATED,
    signup.SetUpStatus.SIGN_UP_VALIDATION: SetUpStatus.SIGN_UP_VALIDATION,
}

def set_user_setup_status(status, user_id=None, user=None):
    if user:
        user.setup_status = SETUP_STATUS_ADAPTER[status]
    if user_id:
        User.objects.filter(id=user_id).update(setup_status = SETUP_STATUS_ADAPTER[status])
