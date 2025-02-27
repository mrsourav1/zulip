from typing import List, Union

from django.utils.translation import gettext as _

from zerver.lib.exceptions import ResourceNotFoundError
from zerver.models import (
    DirectScheduledMessageAPI,
    ScheduledMessage,
    StreamScheduledMessageAPI,
    UserProfile,
)


def access_scheduled_message(
    user_profile: UserProfile, scheduled_message_id: int
) -> ScheduledMessage:
    try:
        return ScheduledMessage.objects.get(id=scheduled_message_id, sender=user_profile)
    except ScheduledMessage.DoesNotExist:
        raise ResourceNotFoundError(_("Scheduled message does not exist"))


def get_undelivered_scheduled_messages(
    user_profile: UserProfile,
) -> List[Union[DirectScheduledMessageAPI, StreamScheduledMessageAPI]]:
    scheduled_messages = ScheduledMessage.objects.filter(
        sender=user_profile, delivered=False, delivery_type=ScheduledMessage.SEND_LATER
    ).order_by("scheduled_timestamp")
    scheduled_message_dicts: List[Union[DirectScheduledMessageAPI, StreamScheduledMessageAPI]] = [
        scheduled_message.to_dict() for scheduled_message in scheduled_messages
    ]
    return scheduled_message_dicts
