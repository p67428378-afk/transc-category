import React from 'react';
import { Line, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement);

const Dashboard = ({ transactions, categories, loading, error }) => {
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
  );
};

export default Dashboard;
