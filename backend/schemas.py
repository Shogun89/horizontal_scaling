from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductCategoryBase(BaseModel):
    name: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategory(ProductCategoryBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    category: ProductCategory

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product: Product

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    total_amount: float
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    order_items: List[OrderItem]

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
