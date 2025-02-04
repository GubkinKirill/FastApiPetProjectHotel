from sqlalchemy import select
from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker

class BookingDAO(BaseDAO):
    model = Booking
    