import React, { useEffect, useState } from 'react';

import DividendTracker from './components/DividendTracker';
import Header from "./components/Header";

const App = () => {
  const [message, setMessage] = useState(null);

  const getWelcomeMessage = async () =>{
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("http://localhost:8000/total_dividends", requestOptions);
    const data = await response.json();

    if (!response.ok){
      console.log("Error");
    }
    else{
      setMessage(data.total_dividends);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);
  
  return (
    <>
      <Header title="ETF Dividend Tracker"/>
      <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-half">
        <DividendTracker />
        </div>
        <div className="column"></div>
      </div>
      
    </>
  );
}

export default App;
