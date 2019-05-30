import enum


class UserRoleEnum(enum.Enum):
    """Class for user roles enum values"""
    user = 'user'
    admin = 'admin'


class TicketStatusEnum(enum.Enum):
    """Class for ticket status enum values"""
    pending = 'pending'
    paid = 'paid'
