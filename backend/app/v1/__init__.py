
from ._utils import create_db_pool, parse_protobuf, close_db_pool, use_event_loop
from .events import event_router, _setup as _event_setup
from .images import image_router


def setup_routers():
    from ._utils import db_pool
    _event_setup(db_pool)
