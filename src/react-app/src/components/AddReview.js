import React, { useState, useEffect } from "react";

const AddReview = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [reviewText, setReviewText] = useState("");
  const [rating, setRating] = useState(1);
  const [successMessage, setSuccessMessage] = useState("");
  const [showRestaurantList, setShowRestaurantList] = useState(true); // To toggle restaurant list

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/restaurants/`, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          Authorization: `Token ${localStorage.getItem("token")}`, // Include token if required
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
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    setShowRestaurantList(true); // Show the list when typing in the search input
  };

  const filteredRestaurants = restaurants.filter((restaurant) =>
    restaurant.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleRestaurantClick = (restaurant) => {
    setSelectedRestaurant(restaurant);
    setShowRestaurantList(false); // Hide the list after selecting a restaurant
  };

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/reviews/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({
          restaurant_id: selectedRestaurant.id,
          review: reviewText,
          rating,
        }),
      });
  
      if (response.ok) {
        setSuccessMessage("Review submitted successfully!");
        setReviewText("");
        setRating(1);
        setSelectedRestaurant(null);
      } else {
        const data = await response.json();
        console.error("Error response:", data);
        alert(data.error || "Failed to submit review.");
      }
    } catch (error) {
      console.error("Error submitting review:", error);
    }
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
            onChange={handleSearch}
            placeholder="Enter restaurant name"
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "15px",
              borderRadius: "5px",
              border: "1px solid #81d4fa",
              boxSizing: "border-box",
            }}
            onFocus={() => setShowRestaurantList(true)} // Show the list when clicking on the input
          />
        </div>
        {showRestaurantList && (
          <ul
            style={{
              maxHeight: "200px",
              overflowY: "auto",
              marginBottom: "15px",
              padding: 0,
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
                    selectedRestaurant?.id === restaurant.id ? "#0288d1" : "#f5f5f5",
                  color: selectedRestaurant?.id === restaurant.id ? "#fff" : "#000",
                  borderBottom: "1px solid #ddd",
                  listStyleType: "none",
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
                step="0.5" // Allow 0.5 step increments
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
      </div>
    </div>
  );
};

export default AddReview;
