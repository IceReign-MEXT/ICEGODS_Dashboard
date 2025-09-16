import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Subscription from "./components/Subscription";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/subscribe" element={<Subscription />} />
      </Routes>
    </Router>
  );
}

export default App;
