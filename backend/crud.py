from sqlalchemy.orm import Session
import models, schemas
from database import get_db_session


def get_product_category(db: Session, category_id: int):
    """
    Retrieve a product category by its ID.

    Args:
        db (Session): The database session.
        category_id (int): The ID of the product category to retrieve.

    Returns:
        models.ProductCategory: The product category object if found, else None.
    """
    return (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
        .first()
    )


def get_product_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of product categories.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.ProductCategory]: A list of product category objects.
    """
    return db.query(models.ProductCategory).offset(skip).limit(limit).all()


def create_product_category(db: Session, category: schemas.ProductCategoryCreate):
    """
    Create a new product category.

    Args:
        db (Session): The database session.
        category (schemas.ProductCategoryCreate): The product category data to create.

    Returns:
        models.ProductCategory: The created product category object.
    """
    db_category = models.ProductCategory(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_product(db: Session, product_id: int):
    """
    Retrieve a product by its ID.

    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to retrieve.

    Returns:
        models.Product: The product object if found, else None.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of products.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.Product]: A list of product objects.
    """
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    """
    Create a new product.

    Args:
        db (Session): The database session.
        product (schemas.ProductCreate): The product data to create.

    Returns:
        models.Product: The created product object.
    """
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_user(db: Session, user_id: int):
    """Get user by ID from this shard"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Get user by email from this shard"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get users from this shard with pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in this shard's database.
    
    Args:
        db (Session): Database session
        user (schemas.UserCreate): User data to create
        
    Returns:
        models.User: Created user object
    """
    db_user = models.User(
        email=user.email,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    """Update user in this shard"""
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Delete user from this shard"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

