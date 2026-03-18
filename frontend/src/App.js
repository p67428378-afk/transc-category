import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';
import './App.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement);

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTransactions();
    fetchCategories();
  }, []);

  const fetchTransactions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/reports/categorized`);
      setTransactions(response.data);
    } catch (err) {
      setError('Failed to fetch transactions.');
      console.error("Error fetching transactions:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/categories`);
      const categoryMap = response.data.reduce((acc, cat) => {
        acc[cat.id] = cat.name;
        return acc;
      }, {});
      setCategories(categoryMap);
    } catch (err) {
      console.error("Error fetching categories:", err);
    }
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post(`${API_BASE_URL}/api/transactions/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('File uploaded and transactions processed successfully!');
      setSelectedFile(null);
      fetchTransactions(); // Refresh transactions after upload
    } catch (err) {
      setError('Failed to upload file or process transactions.');
      console.error("Error uploading file:", err);
    } finally {
      setLoading(false);
    }
  };

  const getSpendingByCategoryData = () => {
    const categorySpending = transactions.reduce((acc, transaction) => {
      const categoryName = categories[transaction.category_id] || 'Uncategorized';
      acc[categoryName] = (acc[categoryName] || 0) + transaction.amount;
      return acc;
    }, {});

    return {
      labels: Object.keys(categorySpending),
      datasets: [
        {
          data: Object.values(categorySpending),
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#4BC0C0',
            '#9966FF',
            '#FF9F40',
            '#5DADE2',
            '#2ECC71',
            '#F1C40F',
            '#E74C3C',
          ],
          hoverBackgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#4BC0C0',
            '#9966FF',
            '#FF9F40',
            '#5DADE2',
            '#2ECC71',
            '#F1C40F',
            '#E74C3C',
          ],
        },
      ],
    };
  };

  const getMonthlyTrendsData = () => {
    const monthlySpending = transactions.reduce((acc, transaction) => {
      const date = new Date(transaction.date);
      const monthYear = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`;
      acc[monthYear] = (acc[monthYear] || 0) + transaction.amount;
      return acc;
    }, {});

    const sortedMonths = Object.keys(monthlySpending).sort();
    const spendingData = sortedMonths.map(month => monthlySpending[month]);

    return {
      labels: sortedMonths,
      datasets: [
        {
          label: 'Monthly Spending',
          data: spendingData,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
      ],
    };
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Transaction Categorization Dashboard</h1>
      </header>
      <main>
        <section className="upload-section">
          <h2>Upload Transactions (CSV)</h2>
          <input type="file" accept=".csv" onChange={handleFileChange} />
          <button onClick={handleFileUpload} disabled={loading || !selectedFile}>
            {loading ? 'Uploading...' : 'Upload & Process'}
          </button>
          {error && <p className="error-message">{error}</p>}
        </section>

        <section className="dashboard-section">
          <h2>Spending Overview</h2>
          {loading && <p>Loading transactions...</p>}
          {!loading && transactions.length === 0 && !error && <p>No transactions uploaded yet. Please upload a CSV.</p>}
          {!loading && transactions.length > 0 && (
            <div className="charts-container">
              <div className="chart-card">
                <h3>Spending by Category</h3>
                <Pie data={getSpendingByCategoryData()} />
              </div>
              <div className="chart-card">
                <h3>Monthly Spending Trends</h3>
                <Line data={getMonthlyTrendsData()} />
              </div>
            </div>
          )}

          {!loading && transactions.length > 0 && (
            <div className="transactions-table-container">
              <h3>All Transactions</h3>
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Description</th>
                    <th>Amount</th>
                    <th>Category</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map((transaction) => (
                    <tr key={transaction.id}>
                      <td>{new Date(transaction.date).toLocaleDateString()}</td>
                      <td>{transaction.original_description}</td>
                      <td>{transaction.amount.toFixed(2)}</td>
                      <td>{categories[transaction.category_id] || 'Uncategorized'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
