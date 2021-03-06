from sqlalchemy import event

from .base.push_id import PushID

from .user import User
from .airplane import Airplane
from .flight import Flight
from .ticket import Ticket


def save_push_id(mapper, connection, target):
    """Function tto run the push id generator and save
    the id on insert
    """
    push_id = PushID()
    target.id = push_id.next_id()


database_tables = [
    User,
    Airplane,
    Flight,
    Ticket,
]

for table in database_tables:  # pragma: no cover
    event.listen(table, 'before_insert', save_push_id)
