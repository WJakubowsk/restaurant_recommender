import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";


const AddReview = () => {

  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [restaurants, setRestaurants] = useState([]);
  const [filteredRestaurants, setFilteredRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [reviewText, setReviewText] = useState("");
  const [rating, setRating] = useState(1);
  const [successMessage, setSuccessMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showRestaurantList, setShowRestaurantList] = useState(true);

  // Fetch all restaurants on component mount
  useEffect(() => {
    fetchRestaurants();
  }, []);

  // Fetch restaurants from the backend
  const fetchRestaurants = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:8000/api/restaurants/`, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        const text = await response.text();
        console.error("Response body:", text);
        throw new Error("HTTP error!");
      }

      const data = await response.json();
      setRestaurants(data.restaurants);
    } catch (error) {
      console.error("Error fetching restaurants:", error);
    } finally {
      setLoading(false);
    }
  };

  // Handle search input change
  const handleSearch = (query) => {
    setSearchQuery(query);
    if (query.length > 0) {
      const filtered = restaurants.filter((restaurant) =>
        restaurant.name.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredRestaurants(filtered);
    } else {
      setFilteredRestaurants([]);
    }
    setShowRestaurantList(true); // Show the list when typing
  };

  // Handle restaurant selection from the dropdown
  const handleRestaurantClick = (restaurant) => {
    setSelectedRestaurant(restaurant);
    setSearchQuery(restaurant.name);
    setFilteredRestaurants([]);
    setShowRestaurantList(false); // Hide the list after selecting
  };

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
  
    const payload = {
      restaurant_name: selectedRestaurant.name.trim(),
      rating: rating,
      text: reviewText,
    };
  
    console.log("Sending payload:", payload); // Debugging
  
    // Reset form state immediately
    setSuccessMessage("Submitting your review...");
    setReviewText("");
    setRating(1);
    setSelectedRestaurant(null);
    setSearchQuery("");
    setShowRestaurantList(false);
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/add_review/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Ensure the correct content type
          "X-CSRFToken": getCSRFToken(),
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(payload),
      });
  
      if (response.ok) {
        setSuccessMessage("Review submitted successfully!");
  
        // Clear the success message after 3 seconds
        setTimeout(() => {
          setSuccessMessage("");
        }, 500);
      } else {
        const data = await response.json();
        console.error("Error response:", data);
        alert(data.error || "Failed to submit review.");
        setSuccessMessage(""); // Clear any pending message
      }
    } catch (error) {
      console.error("Error submitting review:", error);
      alert("An error occurred while submitting your review.");
      setSuccessMessage(""); // Clear any pending message
    }
  };
  

  const getCSRFToken = () => {
    const csrfCookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="));
    return csrfCookie ? csrfCookie.split("=")[1] : "";
  };

  const handleBackToList = () => {
    navigate("/restaurants");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "linear-gradient(135deg, #e0f7fa, #81d4fa)",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "30px 40px",
          borderRadius: "10px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
          width: "100%",
          maxWidth: "500px",
        }}
      >
        <h1
          style={{
            fontSize: "24px",
            marginBottom: "20px",
            textAlign: "center",
            color: "#0277bd",
          }}
        >
          Add Review
        </h1>
        <div>
          <label style={{ fontWeight: "bold", display: "block", marginBottom: "5px" }}>
            Search Restaurant:
          </label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder="Enter restaurant name"
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "15px",
              borderRadius: "5px",
              border: "1px solid #81d4fa",
              boxSizing: "border-box",
            }}
            onFocus={() => setShowRestaurantList(true)} // Show the list when focusing
          />
        </div>
        {loading && <p>Loading restaurants...</p>}
        {showRestaurantList && filteredRestaurants.length > 0 && (
          <ul
            style={{
              maxHeight: "200px",
              overflowY: "auto",
              marginBottom: "15px",
              padding: 0,
              listStyleType: "none",
              border: "1px solid #ddd",
              borderRadius: "5px",
              backgroundColor: "white",
            }}
          >
            {filteredRestaurants.map((restaurant) => (
              <li
                key={restaurant.id}
                onClick={() => handleRestaurantClick(restaurant)}
                style={{
                  padding: "10px",
                  cursor: "pointer",
                  backgroundColor:
                    selectedRestaurant?.id === restaurant.id ? "#0288d1" : "#fff",
                  color: selectedRestaurant?.id === restaurant.id ? "#fff" : "#000",
                  borderBottom: "1px solid #ddd",
                }}
              >
                {restaurant.name}
              </li>
            ))}
          </ul>
        )}
        {selectedRestaurant && (
          <form onSubmit={handleSubmitReview}>
            <h2 style={{ fontSize: "18px", marginBottom: "15px", color: "#0277bd" }}>
              Review {selectedRestaurant.name}
            </h2>
            <div>
              <label
                style={{
                  fontWeight: "bold",
                  display: "block",
                  marginBottom: "5px",
                }}
              >
                Rating (1-5):
              </label>
              <input
                type="number"
                value={rating}
                onChange={(e) => setRating(Number(e.target.value))}
                min="1"
                max="5"
                step="0.5"
                required
                style={{
                  width: "100%",
                  padding: "10px",
                  marginBottom: "15px",
                  borderRadius: "5px",
                  border: "1px solid #81d4fa",
                  boxSizing: "border-box",
                }}
              />
            </div>
            <div>
              <label
                style={{
                  fontWeight: "bold",
                  display: "block",
                  marginBottom: "5px",
                }}
              >
                Review:
              </label>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="Write your review here"
                required
                style={{
                  width: "100%",
                  height: "100px",
                  padding: "10px",
                  borderRadius: "5px",
                  border: "1px solid #81d4fa",
                  boxSizing: "border-box",
                  marginBottom: "15px",
                }}
              ></textarea>
            </div>
            <button
              type="submit"
              style={{
                width: "100%",
                padding: "10px",
                backgroundColor: "#0288d1",
                color: "white",
                fontSize: "16px",
                fontWeight: "bold",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                transition: "background-color 0.3s",
              }}
              onMouseOver={(e) => (e.target.style.backgroundColor = "#01579b")}
              onMouseOut={(e) => (e.target.style.backgroundColor = "#0288d1")}
            >
              Submit Review
            </button>
          </form>
        )}
        {successMessage && (
          <p
            style={{
              color: "green",
              marginTop: "15px",
              textAlign: "center",
              fontSize: "14px",
            }}
          >
            {successMessage}
          </p>
        )}
        <button
          onClick={handleBackToList}
          style={{
            marginTop: "20px",
            width: "100%",
            padding: "10px",
            backgroundColor: "#0288d1",
            color: "white",
            fontSize: "16px",
            fontWeight: "bold",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
            transition: "background-color 0.3s",
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#01579b")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#0288d1")}
        >
          Back to Restaurant List
        </button>
      </div>
    </div>
  );
};

export default AddReview;
