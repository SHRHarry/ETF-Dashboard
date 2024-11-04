import React, { useState, useEffect } from 'react';
import axios from 'axios';
import moment from "moment";

import "./TableStyles.css";
import PieChart from './PieChart';
import StockModal from "./StockModal";

const DividendTracker = () => {
  const [totalDividends, setTotalDividends] = useState(null);
  const [allStocks, setAllStocks] = useState(null);
  const [individualDividends, setIndividualDividends] = useState([]);
  const [pieData, setPieData] = useState({ labels: [], values: [] });
  const [loading, setLoading] = useState(true);
  const [activeModal, setActiveModal] = useState(false);
  const [id, setId] = useState(null);
  const [purchaseDate, setPurchaseDate] = useState(new Date().toISOString().substring(0, 10));
  const [error, setError] = useState(null);

  const handleUpdate = async (id) => {
    setId(id);
    setActiveModal(true);
  };

  const handleDelete = async (id) => {
    try{
      const response = await axios.delete(`http://localhost:8000/individual_stock_dividends/${id}`);
    } catch (error) {
      setError('Failed to delete individual stock by id');
    }
    getAllStocks();
    getTotalDividends();
  };

  const deleteTotalDividends = async (id) => {
    try{
      const response = await axios.delete('http://localhost:8000/total_dividends');
      setLoading(false);
    } catch (error){
      setError('Failed to delete individual stock');
      setLoading(false);
    }
    getAllStocks();
    getTotalDividends();
    setPieData({ labels: [], values: [] });
  };

  const handleModal = () => {
    setActiveModal(!activeModal);
    getAllStocks();
    setId(null);
    setPurchaseDate(null);
  };
  
  useEffect(() => {
    getTotalDividends();
  }, []);

  useEffect(() => {
    getAllStocks();
  }, []);

  useEffect(() => {
    if (individualDividends.length > 0) {
      const labels = individualDividends.map(stock => `${stock.symbol}`);
      const values = individualDividends.map(stock => stock.receive_dividends);
      const total = values.reduce((acc, value) => acc + value, 0);
      const percentages = values.map(value => (value / total) * 100);

      setPieData({ labels, values: percentages });
    }
  }, [individualDividends]);

  const getTotalDividends = async () => {
    try {
      const response = await axios.get('http://localhost:8000/total_dividends');
      setTotalDividends(response.data.total_dividends);
      setLoading(false);
    } catch (error) {
      setError('Failed to fetch total dividends');
      setLoading(false);
    }
  };

  const getAllStocks = async () => {
    try {
      const response = await axios.get('http://localhost:8000/all_stocks');
      setAllStocks(response.data);
      const stockSymbols = Array.from(new Set(response.data.map(stock => stock.symbol)));
      stockSymbols.forEach(symbol => fetchIndividualDividends(symbol));
      setLoading(false);
    } catch (error) {
      setError('Failed to fetch all stocks');
      setLoading(false);
    }
  };

  const fetchIndividualDividends = async (symbol) => {
    try {
      setIndividualDividends([]);
      const response = await axios.get(`http://localhost:8000/individual_stock_dividends?symbol=${symbol}`);
      setIndividualDividends((prevStocks) => [...prevStocks, response.data]);
    } catch (error) {
      setError('Failed to fetch individual stock dividends');
    }
  };

  return (
    <>
    <div className="column m-5 is-one-third">
      <StockModal
        active={activeModal}
        handleModal={handleModal}
        id={id}
        setError={setError}
        getTotalDividends={getTotalDividends}
      />
      <section class="info-tiles m-3">
          <div class="tile is-ancestor has-text-centered">
              <div class="tile is-parent">
                  <article class="tile is-child box">
                      <p class="title">${totalDividends}</p>
                      <p class="subtitle">Total Dividends</p>
                      {pieData.labels.length && <PieChart data={pieData} />}
                  </article>
              </div>
          </div>
      </section>
    </div>
    <div className="column m-5 is-half">
    <div className="columns is-centered is-gapless m-3">
      <div className="column is-half">
        <button
          className="button is-fullwidth is-success"
          style={{
            borderTopRightRadius: 0,
            borderBottomRightRadius: 0,
            borderRight: '1px solid #ccc'
          }}
          onClick={() => setActiveModal(true)}
        >
          Add Stock
        </button>
      </div>
      <div className='column is-half'>
        <button
          className="button is-fullwidth is-danger"
          style={{
            borderTopLeftRadius: 0,
            borderBottomLeftRadius: 0
          }}
          onClick={() => deleteTotalDividends()}
        >
          Delete All Stock
        </button>
      </div>
    </div>
    
    {loading ? (
      <p>Loading...</p>
    ) : error || !allStocks ? (
      <p>{error}</p>
    ) : (
      <div className='table-container'>
        <table className="table is-fullwidth">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Shares</th>
            <th>Purchase Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
        {allStocks.map((allStock) => (
              <tr key={allStock.id}>
                <td>{allStock.symbol}</td>
                <td>{allStock.shares}</td>
                <td>{moment(allStock.purchase_date).format("YYYY-MM-DD")}</td>
                <td>
                  <button
                    className="button mr-2 is-info is-light"
                    onClick={() => handleUpdate(allStock.id)}
                  >
                    Update
                  </button>
                  <button
                    className="button mr-2 is-danger is-light"
                    onClick={() => handleDelete(allStock.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
      </table>
      </div>
    )}
    </div>
    </>
  );
};

export default DividendTracker;