from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from datetime import datetime # Added import

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, username=user.username, password_hash=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_or_create_category(db: Session, category_name: str):
    category = get_category_by_name(db, category_name)
    if not category:
        category = models.Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_transaction_by_hash(db: Session, raw_data_hash: str):
    return db.query(models.Transaction).filter(models.Transaction.raw_data_hash == raw_data_hash).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    # This function also needs to handle date conversion if it's used directly
    # For now, focusing on get_or_create_transactions as per the prompt
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_or_create_transactions(db: Session, transactions_data: List[schemas.TransactionCreate]):
    new_transactions = []
    for transaction_data in transactions_data:
        existing_transaction = get_transaction_by_hash(db, transaction_data.raw_data_hash)
        if not existing_transaction:
            # Convert date string to datetime object
            transaction_date = datetime.fromisoformat(transaction_data.date) # Modified line
            db_transaction = models.Transaction(
                user_id=transaction_data.user_id,
                original_description=transaction_data.original_description,
                amount=transaction_data.amount,
                date=transaction_date, # Modified line
                raw_data_hash=transaction_data.raw_data_hash
            )
            db.add(db_transaction)
            new_transactions.append(db_transaction)
        else:
            new_transactions.append(existing_transaction) # Include existing ones in the return

    db.commit()
    for transaction in new_transactions:
        db.refresh(transaction)
    return new_transactions

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()
