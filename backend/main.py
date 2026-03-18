from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
import hashlib

from . import crud, models, schemas, database, llm_integration

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)

@app.post("/api/transactions/upload", response_model=List[schemas.Transaction])
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

    # Basic cleaning and standardization (HLD Step 3.2 - ETL Trigger)
    # Assuming CSV has 'date', 'description', 'amount' columns
    df.columns = df.columns.str.lower()
    required_columns = ['date', 'description', 'amount']
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(status_code=400, detail=f"CSV must contain columns: {', '.join(required_columns)}")

    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])
    df['original_description'] = df['description']

    # Generate raw_data_hash for deduplication
    df['raw_data_hash'] = df.apply(lambda row: hashlib.sha256(str(row[['date', 'description', 'amount']]).encode('utf-8')).hexdigest(), axis=1)

    transactions_to_create = []
    for index, row in df.iterrows():
        transaction_data = schemas.TransactionCreate(
            user_id=1, # TODO: Implement actual user management and get user_id from auth
            original_description=row['original_description'],
            amount=row['amount'],
            date=row['date'].isoformat(),
            raw_data_hash=row['raw_data_hash']
        )
        transactions_to_create.append(transaction_data)
    
    # Deduplicate before saving (HLD Step 4.6 - Data Integrity & Consistency)
    new_transactions = crud.get_or_create_transactions(db, transactions_to_create)

    # Trigger categorization for new transactions (HLD Step 3.1 - Categorization Service)
    categorized_transactions = []
    for transaction in new_transactions:
        if not transaction.category_id:
            # This is where the LLM categorization would be called
            predicted_category_name = llm_integration.categorize_transaction_with_llm(transaction.original_description)
            category = crud.get_or_create_category(db, predicted_category_name)
            transaction.category_id = category.id
            transaction.categorized_by = "LLM"
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
        categorized_transactions.append(transaction)

    return categorized_transactions

@app.get("/api/reports/categorized", response_model=List[schemas.Transaction])
def get_categorized_transactions(db: Session = Depends(get_db)):
    # TODO: Implement filtering by user_id once auth is in place
    transactions = crud.get_transactions(db)
    return transactions

@app.get("/api/categories", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories
