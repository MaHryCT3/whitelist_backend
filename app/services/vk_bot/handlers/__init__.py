from .applications import application_labeler
from .notifications import notifications_labeler
from .whiltelist import whitelist_labeler

labelers = [application_labeler, whitelist_labeler, notifications_labeler]
