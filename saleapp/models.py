from sqlalchemy import Column, Integer, Float, \
    String, ForeignKey, Boolean, Date, Enum, DateTime
from sqlalchemy.orm import relationship
from saleapp import db
from flask_login import UserMixin
from enum import Enum as UserEnum
from datetime import datetime


class SaleBase(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Category(SaleBase):
    __tablename__ = 'category'

    products = relationship('Product',
                            backref='category',
                            lazy=True)


class Product(SaleBase):
    __tablename__ = 'product'

    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(255))
    category_id = Column(Integer,
                         ForeignKey(Category.id),
                         nullable=False)

    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class User(SaleBase, UserMixin):
    __tablename__ = 'user'

    email = Column(String(50))
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    is_active = Column(Boolean, default=True)
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    receipts = relationship('Receipt', backref='user', lazy=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(User.id))

    details = relationship('ReceiptDetail',
                           backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id))
    receipt_id = Column(Integer, ForeignKey(Receipt.id))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)


if __name__ == '__main__':
    db.create_all()
