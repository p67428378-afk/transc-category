import pandas as pd
import hashlib
import requests
import os
from datetime import datetime

# Configuration for the Backend API
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend:8000")

def process_csv_data(file_path: str, user_id: int):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    df.columns = df.columns.str.lower() # Standardize column names

    required_columns = ['date', 'description', 'amount']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: CSV must contain columns: {', '.join(required_columns)}")
        return

    # Data Cleaning and Standardization
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])
    df['original_description'] = df['description'] # Keep original description

    # Deduplication: Generate a hash for each transaction based on key fields
    df['raw_data_hash'] = df.apply(lambda row: hashlib.sha256(str(row[['date', 'description', 'amount']]).encode('utf-8')).hexdigest(), axis=1)

    # Prepare data for API submission
    transactions_payload = []
    for index, row in df.iterrows():
        transactions_payload.append({
            "user_id": user_id,
            "original_description": row['original_description'],
            "amount": row['amount'],
            "date": row['date'].isoformat(),
            "raw_data_hash": row['raw_data_hash']
        })
    
    # Send to Backend API for saving and categorization
    upload_url = f"{BACKEND_API_URL}/api/transactions/upload"
    try:
        # The backend expects a file-like object for upload, not a JSON payload for this endpoint.
        # This ETL script is designed to process a local CSV and then send it to the backend.
        # For simplicity, we'll simulate the file upload by re-creating a file-like object.
        # In a real-world scenario, the ETL might directly interact with the database or a message queue
        # after processing, or the backend might expose a different endpoint for processed data.
        
        # For now, let's assume the backend's /api/transactions/upload expects a multipart/form-data
        # with a 'file' field. This ETL service would then be responsible for reading the CSV and
        # sending it as a file.
        
        # Re-creating the CSV in memory to send as a file
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        files = {'file': (os.path.basename(file_path), output.getvalue(), 'text/csv')}
        response = requests.post(upload_url, files=files)
        response.raise_for_status() # Raise an exception for HTTP errors
        print("ETL Processed and uploaded transactions successfully!")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error uploading transactions to backend: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Backend response: {e.response.text}")

if __name__ == "__main__":
    # Example usage: This would typically be triggered by an event or scheduler
    # For local testing, place a sample.csv in the data_engineering directory
    sample_csv_path = "./sample.csv"
    if os.path.exists(sample_csv_path):
        print(f"Processing {sample_csv_path}...")
        # Assuming a default user_id for now, replace with actual user_id from context
        process_csv_data(sample_csv_path, user_id=1)
    else:
        print(f"{sample_csv_path} not found. Please create a sample.csv for testing.")
        print("Example sample.csv content:")
        print("date,description,amount\n2023-01-01,Starbucks Coffee,5.50\n2023-01-02,Monthly Rent,1200.00\n2023-01-03,Electricity Bill,75.20\n2023-01-04,Walmart Groceries,150.30")
