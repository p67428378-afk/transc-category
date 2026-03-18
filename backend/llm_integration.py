import os

def categorize_transaction_with_llm(description: str) -> str:
    # This is a placeholder for actual LLM integration.
    # In a real scenario, this would call an external LLM API (e.g., Google Gemini, OpenAI).
    # For now, we'll use a very basic keyword-based categorization.
    
    description_lower = description.lower()

    if any(keyword in description_lower for keyword in ["starbucks", "coffee", "cafe", "bakery"]):
        return "Food & Drink"
    elif any(keyword in description_lower for keyword in ["rent", "mortgage"]):
        return "Housing"
    elif any(keyword in description_lower for keyword in ["electricity", "water", "gas", "utility"]):
        return "Utilities"
    elif any(keyword in description_lower for keyword in ["supermarket", "grocery", "walmart", "target"]):
        return "Groceries"
    elif any(keyword in description_lower for keyword in ["salary", "paycheck"]):
        return "Income"
    elif any(keyword in description_lower for keyword in ["amazon", "retail", "store"]):
        return "Shopping"
    elif any(keyword in description_lower for keyword in ["bus", "train", "uber", "taxi"]):
        return "Transportation"
    elif any(keyword in description_lower for keyword in ["gym", "fitness", "doctor", "pharmacy"]):
        return "Health & Wellness"
    elif any(keyword in description_lower for keyword in ["movie", "concert", "bar"]):
        return "Entertainment"
    
    return "Uncategorized"
