import React, { useEffect, useState } from 'react';

const IBSBalance = () => {
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/balance`)
      .then(res => res.json())
      .then(data => setBalance(data.balance))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h3>Your ICEGODS Balance: {balance} ICE</h3>
    </div>
  );
};

export default IBSBalance;
