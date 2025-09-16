import React from "react";
import { Link } from "react-router-dom";
import BotTracker from "./BotTracker";
import ParticlesBackground from "./ParticlesBackground";

const Dashboard = () => {
  return (
    <div>
      <ParticlesBackground />
      <h1>ICEGODS Dashboard</h1>
      <BotTracker />
      <Link to="/subscribe">
        <button>Subscribe Now</button>
      </Link>
    </div>
  );
};

export default Dashboard;
