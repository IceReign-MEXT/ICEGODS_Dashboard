import React from "react";

function Dashboard({ user }) {
  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-lg">
      <h2 className="text-2xl font-bold text-center mb-4 text-green-400">
        Welcome, {user.email} 🎉
      </h2>
      <p className="text-center text-gray-300 mb-4">
        You’re now inside the ICEGODS Dashboard.
      </p>
      <ul className="space-y-2 text-left">
        <li>📊 Track wallet activity</li>
        <li>💳 Manage subscription</li>
        <li>⚡ View real-time updates</li>
      </ul>
    </div>
  );
}

export default Dashboard;
