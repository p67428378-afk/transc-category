const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const uploadTransactions = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/transactions/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to upload transactions');
  }
  return response.json();
};

export const getCategorizedTransactions = async () => {
  const response = await fetch(`${API_BASE_URL}/api/reports/categorized`);
  if (!response.ok) {
    throw new Error('Failed to fetch categorized transactions');
  }
  return response.json();
};

export const getCategories = async () => {
  const response = await fetch(`${API_BASE_URL}/api/categories`);
  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }
  return response.json();
};
