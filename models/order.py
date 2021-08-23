from operator import delitem
import os

from db import db
from typing import List

class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(20), nullable = False)

    items = db.relationship("ItemModel", lazy="dynamic")

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()