import React, { useEffect, useState } from "react";
import axios from 'axios';
import moment from "moment";

const StockModal = ({ active, handleModal, id, setError, getTotalDividends, getCurrentMonthDividends}) => {
    const [symbol, setSymbol] = useState("");
    const [shares, setShares] = useState("");
    const [purchaseDate, setPurchaseDate] = useState(new Date().toISOString().substring(0, 10));

    useEffect(() => {
        const getStockById = async () => {
            try {
                const response = await axios.get(`https://etf-dashboard-1.onrender.com/individual_stock_dividends/${id}`);
                setSymbol(response.data.symbol);
                setShares(response.data.shares);
                setPurchaseDate(moment(response.data.purchase_date).format("YYYY-MM-DD"));
            } catch (error) {
                setError("Failed to get stock by id");
            }
    
        };
    
        if (id) {
            getStockById();
            getTotalDividends();
            getCurrentMonthDividends();
        }
      }, [id]);
    
      const cleanFormData = () => {
        setSymbol("");
        setShares("");
        setPurchaseDate("");
      };
    
      const handleCreateStock = async (e) => {
        e.preventDefault();
        const url = `https://etf-dashboard-1.onrender.com/individual_stock_dividends`;
        const data = {
            symbol: symbol,
            shares: shares,
            purchase_date: purchaseDate,
        };
        try {
            const response = await axios.post(url, data);
            cleanFormData();
            handleModal();
            getTotalDividends();
            getCurrentMonthDividends();
          } catch (error) {
            setError('Error creating stock dividends:', error);
          }
      };
    
      const handleUpdateStock = async (e) => {
        e.preventDefault();
        const url = `https://etf-dashboard-1.onrender.com/individual_stock_dividends/${id}`;
        const data = {
            symbol: symbol,
            shares: shares,
            purchase_date: purchaseDate,
        };
        try {
            const response = await axios.put(url, data);
            cleanFormData();
            handleModal();
            getTotalDividends();
            getCurrentMonthDividends();
          } catch (error) {
            setError('Error creating stock dividends:', error);
          }
      };
    
    return (
        <div className={`modal ${active && "is-active"}`}>
          <div className="modal-background" onClick={handleModal}></div>
          <div className="modal-card">
            <header className="modal-card-head has-background-primary-light">
              <h1 className="modal-card-title">
                {id ? "Update Lead" : "Create Lead"}
              </h1>
            </header>
            <section className="modal-card-body">
              <form>
                <div className="field">
                  <label className="label">Symbol</label>
                  <div className="control">
                    <input
                      type="text"
                      placeholder="Enter symbol"
                      value={symbol}
                      onChange={(e) => setSymbol(e.target.value)}
                      className="input"
                      required
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label">Shares</label>
                  <div className="control">
                    <input
                      type="number"
                      placeholder="Enter shares"
                      value={shares}
                      onChange={(e) => setShares(e.target.value)}
                      className="input"
                      required
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label">Date</label>
                  <div className="control">
                    <input
                      type="date"
                      placeholder="Enter date"
                      value={purchaseDate}
                      onChange={(e) => setPurchaseDate(e.target.value)}
                      className="input"
                    />
                  </div>
                </div>
              </form>
            </section>
            <footer className="modal-card-foot has-background-primary-light">
              {id ? (
                <button className="button is-info" onClick={handleUpdateStock}>
                  Update
                </button>
              ) : (
                <button className="button is-primary" onClick={handleCreateStock}>
                  Create
                </button>
              )}
              <button className="button" onClick={handleModal}>
                Cancel
              </button>
            </footer>
          </div>
        </div>
      );
};

export default StockModal;
