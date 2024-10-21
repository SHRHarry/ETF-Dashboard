import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DividendTracker = () => {
  const [totalDividends, setTotalDividends] = useState(null);
  const [individualDividends, setIndividualDividends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTotalDividends();
  }, []);

  const fetchTotalDividends = async () => {
    try {
      const response = await axios.get('http://localhost:8000/total_dividends');
      setTotalDividends(response.data.total_dividends);
      setLoading(false);
    } catch (error) {
      setError('Failed to fetch total dividends');
      setLoading(false);
    }
  };

  const fetchIndividualDividends = async (symbol) => {
    try {
      const response = await axios.get(`http://localhost:8000/individual_stock_dividends?symbol=${symbol}`);
      setIndividualDividends(response.data);
    } catch (error) {
      setError('Failed to fetch individual stock dividends');
    }
  };

  return (
    <div>
      <h1>ETF Dividend Tracker</h1>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <div>
          <h2>Total Dividends: {totalDividends}</h2>
          <h3>Individual Stock Dividends:</h3>
          <button onClick={() => fetchIndividualDividends('0056')}>Fetch Dividends for 0056</button>
          <button onClick={() => fetchIndividualDividends('00878')}>Fetch Dividends for 00878</button>
          <button onClick={() => fetchIndividualDividends('00919')}>Fetch Dividends for 00919</button>
          <div>
            {individualDividends && (
              <ul>
                <li>Symbol: {individualDividends.symbol}</li>
                <li>Receive Dividends: {individualDividends.receive_dividends}</li>
                <li>Receive Shares: {individualDividends.receive_shares}</li>
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DividendTracker;