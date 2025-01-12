import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import RestaurantList from "./components/RestaurantList";
import Signup from "./components/Signup";
import Login from "./components/Login";
import AddReview from "./components/AddReview";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <Routes>
        {/* Default route: Navigate to Login if not logged in */}
        <Route path="/" element={isLoggedIn ? <RestaurantList /> : <Navigate to="/login" />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/restaurants" element={isLoggedIn ? <RestaurantList /> : <Navigate to="/login" />} />
         {/* Add the new Add Review route */}
        <Route path="/add-review" element={isLoggedIn ? <AddReview /> : <Navigate to="/login" />} />

      </Routes>
    </Router>
  );
};

export default App;
