from config.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
import pytz
from datetime import datetime


class CamerasDataModel(Base):
    __tablename__ = "cameras_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=lambda: pytz.timezone('Etc/GMT+8').localize(datetime.now()))
    image_base64 = Column(Text, nullable=False)
    camera_id = Column(String, nullable=False)
