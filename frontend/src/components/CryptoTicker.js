import React, { useEffect, useState } from 'react';

const CryptoTicker = () => {
  const [price, setPrice] = useState(null);

  useEffect(() => {
    fetch('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
      .then(res => res.json())
      .then(data => setPrice(data.ethereum.usd))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h3>ETH Price: {price ? `$${price}` : 'Loading...'}</h3>
    </div>
  );
};

export default CryptoTicker;
