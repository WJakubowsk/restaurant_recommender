import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const RestaurantList = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [filters, setFilters] = useState({
    name: "",
    cuisine: "",
    ambience: "",
    min_rating: "",
    city: "",
    price_range: "",
    open_now: false,
    delivery: false,
    good_for_kids: false,
    good_for_groups: false,
    take_out: false,
    reservations: false,
    outdoor_seating: false,
    wheelchair_accessible: false,
    bike_parking: false,
    credit_cards_accepted: false,
    happy_hour: false,
    dogs_allowed: false,
    sustainable: false,
  });
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [filtersApplied, setFiltersApplied] = useState(false);
  const [showTable, setShowTable] = useState(true);
  const [showMap, setShowMap] = useState(true);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const fetchRestaurants = async () => {
    const allRestaurants = [
      {
        name: "Restaurant A",
        cuisine: "Italian",
        ambience: "Cozy",
        min_rating: "4.5",
        city: "New York",
        price_range: "$$$",
        delivery: true,
        good_for_kids: true,
        good_for_groups: true,
        take_out: true,
        reservations: true,
        outdoor_seating: true,
        wheelchair_accessible: true,
        bike_parking: true,
        credit_cards_accepted: true,
        happy_hour: true,
        dogs_allowed: false,
        sustainable: true,
        latitude: 40.7128,
        longitude: -74.006,
      },
      {
        name: "Restaurant B",
        cuisine: "French",
        ambience: "Romantic",
        min_rating: "4.0",
        city: "Paris",
        price_range: "$$",
        delivery: false,
        good_for_kids: false,
        good_for_groups: true,
        take_out: false,
        reservations: true,
        outdoor_seating: false,
        wheelchair_accessible: true,
        bike_parking: false,
        credit_cards_accepted: true,
        happy_hour: false,
        dogs_allowed: true,
        sustainable: false,
        latitude: 48.8566,
        longitude: 2.3522,
      },
      ...Array.from({ length: 50 }, (_, i) => ({
        name: `Restaurant ${i + 1}`,
        cuisine: "Global",
        ambience: "Casual",
        min_rating: (Math.random() * 5).toFixed(1),
        city: `City ${i + 1}`,
        price_range: "$$",
        delivery: Math.random() > 0.5,
        good_for_kids: Math.random() > 0.5,
        good_for_groups: Math.random() > 0.5,
        take_out: Math.random() > 0.5,
        reservations: Math.random() > 0.5,
        outdoor_seating: Math.random() > 0.5,
        wheelchair_accessible: Math.random() > 0.5,
        bike_parking: Math.random() > 0.5,
        credit_cards_accepted: Math.random() > 0.5,
        happy_hour: Math.random() > 0.5,
        dogs_allowed: Math.random() > 0.5,
        sustainable: Math.random() > 0.5,
        latitude: Math.random() * 180 - 90,
        longitude: Math.random() * 360 - 180,
      })),
    ];

    const isFilterApplied = Object.values(filters).some(
      (value) => value !== "" && value !== false
    );

    const filteredRestaurants = isFilterApplied
      ? allRestaurants.filter((restaurant) =>
          Object.entries(filters).every(([key, value]) => {
            if (typeof value === "boolean") return restaurant[key] === value;
            if (value === "") return true;
            return restaurant[key]?.toString().toLowerCase().includes(value.toLowerCase());
          })
        )
      : allRestaurants;

    setRestaurants(filteredRestaurants);
  };

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    setFiltersApplied(true);
    fetchRestaurants();
  };

  const toggleButtonFilter = (field) => {
    setFilters((prev) => ({
      ...prev,
      [field]: !prev[field],
    }));
  };

  const handleRowClick = (restaurant) => {
    setSelectedRestaurant(restaurant); // Set the selected restaurant for zooming
  };

  const MapFocus = ({ position }) => {
    const map = useMap();
    useEffect(() => {
      if (position) {
        map.flyTo(position, 10, { duration: 0.5 }); // Fly to the restaurant with zoom level 15
      }
    }, [position, map]);
    return null;
  };

  return (
    <div style={styles.container}>
      {/* Sidebar */}
      {isSidebarVisible && (
        <div style={styles.sidebar}>
          <h2 style={styles.sidebarTitle}>Filters</h2>
          <form onSubmit={handleFilterSubmit} style={styles.form}>
            <label style={styles.label}>
              Restaurant name:
              <input
                type="text"
                name="name"
                value={filters.name}
                onChange={(e) =>
                  setFilters({ ...filters, name: e.target.value })
                }
                style={styles.input}
                placeholder="Search by name"
              />
            </label>
            <label style={styles.label}>
              Cuisine:
              <input
                type="text"
                name="cuisine"
                value={filters.cuisine}
                onChange={(e) =>
                  setFilters({ ...filters, cuisine: e.target.value })
                }
                style={styles.input}
              />
            </label>
            <label style={styles.label}>
              Ambience:
              <input
                type="text"
                name="ambience"
                value={filters.ambience}
                onChange={(e) =>
                  setFilters({ ...filters, ambience: e.target.value })
                }
                style={styles.input}
              />
            </label>
            <label style={styles.label}>
              Min Rating:
              <input
                type="number"
                name="min_rating"
                value={filters.min_rating}
                onChange={(e) =>
                  setFilters({ ...filters, min_rating: e.target.value })
                }
                style={styles.input}
              />
            </label>
            <label style={styles.label}>
              City:
              <input
                type="text"
                name="city"
                value={filters.city}
                onChange={(e) => setFilters({ ...filters, city: e.target.value })}
                style={styles.input}
              />
            </label>
            <label style={styles.label}>
              Price Range:
              <input
                type="text"
                name="price_range"
                value={filters.price_range}
                onChange={(e) =>
                  setFilters({ ...filters, price_range: e.target.value })
                }
                style={styles.input}
              />
            </label>

            {/* Button Filters */}
            <div style={styles.buttonFilters}>
              {[
                { label: "Open Now", field: "open_now" },
                { label: "Delivery", field: "delivery" },
                { label: "Good for Kids", field: "good_for_kids" },
                { label: "Good for Groups", field: "good_for_groups" },
                { label: "Take Out", field: "take_out" },
                { label: "Reservations", field: "reservations" },
                { label: "Outdoor Seating", field: "outdoor_seating" },
                { label: "Wheelchair Accessible", field: "wheelchair_accessible" },
                { label: "Bike Parking", field: "bike_parking" },
                { label: "Credit Cards Accepted", field: "credit_cards_accepted" },
                { label: "Happy Hour", field: "happy_hour" },
                { label: "Dogs Allowed", field: "dogs_allowed" },
                { label: "Sustainable", field: "sustainable" },
              ].map(({ label, field }) => (
                <button
                  key={field}
                  type="button"
                  onClick={() => toggleButtonFilter(field)}
                  style={{
                    ...styles.filterButton,
                    backgroundColor: filters[field] ? "#0288d1" : "#81d4fa",
                  }}
                >
                  {label}
                </button>
              ))}
            </div>

            <button type="submit" style={styles.button}>
              Apply Filters
            </button>
          </form>
        </div>
      )}

      {/* Main Content */}
      <div style={styles.mainContent}>
        <div style={styles.toggleButtons}>
          <button
            onClick={() => setIsSidebarVisible(!isSidebarVisible)}
            style={styles.toggleButton}
          >
            {isSidebarVisible ? "Hide Filters" : "Show Filters"}
          </button>
          <button
            onClick={() => setShowTable(!showTable)}
            style={styles.toggleButton}
          >
            {showTable ? "Hide Table" : "Show Table"}
          </button>
          <button
            onClick={() => setShowMap(!showMap)}
            style={styles.toggleButton}
          >
            {showMap ? "Hide Map" : "Show Map"}
          </button>
        </div>

        {filtersApplied && (
          <div style={styles.results}>
            {/* Results Table */}
            {showTable && (
              <div style={styles.tableContainer}>
                <h2 style={styles.tableTitle}>Restaurants</h2>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>Name</th>
                      <th style={styles.th}>Cuisine</th>
                      <th style={styles.th}>City</th>
                      <th style={styles.th}>Rating</th>
                      <th style={styles.th}>Price Range</th>
                      <th style={styles.th}>Delivery</th>
                    </tr>
                  </thead>
                  <tbody>
                    {restaurants.map((restaurant, index) => (
                      <tr
                        key={index}
                        style={{ cursor: "pointer" }}
                        onClick={() => handleRowClick(restaurant)}
                      >
                        <td style={styles.td}>{restaurant.name}</td>
                        <td style={styles.td}>{restaurant.cuisine}</td>
                        <td style={styles.td}>{restaurant.city}</td>
                        <td style={styles.td}>{restaurant.min_rating}</td>
                        <td style={styles.td}>{restaurant.price_range}</td>
                        <td style={styles.td}>
                          {restaurant.delivery ? "Yes" : "No"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Map */}
            {showMap && (
              <div style={styles.mapContainer}>
                <MapContainer
                  center={
                    selectedRestaurant
                      ? [selectedRestaurant.latitude, selectedRestaurant.longitude]
                      : [0, 0]
                  }
                  zoom={2}
                  style={{ height: "100%", width: "100%" }}
                >
                  <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                  {selectedRestaurant && (
                    <MapFocus
                      position={[
                        selectedRestaurant.latitude,
                        selectedRestaurant.longitude+0.4,
                      ]}
                    />
                  )}
                  {restaurants.map((restaurant, index) => (
                    <Marker
                      key={index}
                      position={[restaurant.latitude, restaurant.longitude]}
                    >
                      <Popup>
                        <b>{restaurant.name}</b>
                        <br />
                        <b>Cuisine:</b> {restaurant.cuisine}
                        <br />
                        <b>Ambience:</b> {restaurant.ambience}
                        <br />
                        <b>City:</b> {restaurant.city}
                        <br />
                        <b>Rating:</b> {restaurant.min_rating} stars
                        <br />
                        <b>Price Range:</b> {restaurant.price_range}
                        <br />
                        <b>Delivery:</b> {restaurant.delivery ? "Yes" : "No"}
                        <br />
                        <b>Good for Kids:</b> {restaurant.good_for_kids ? "Yes" : "No"}
                        <br />
                        <b>Good for Groups:</b> {restaurant.good_for_groups ? "Yes" : "No"}
                        <br />
                        <b>Take Out:</b> {restaurant.take_out ? "Yes" : "No"}
                        <br />
                        <b>Reservations:</b> {restaurant.reservations ? "Yes" : "No"}
                        <br />
                        <b>Outdoor Seating:</b>{" "}
                        {restaurant.outdoor_seating ? "Yes" : "No"}
                        <br />
                        <b>Wheelchair Accessible:</b>{" "}
                        {restaurant.wheelchair_accessible ? "Yes" : "No"}
                        <br />
                        <b>Bike Parking:</b> {restaurant.bike_parking ? "Yes" : "No"}
                        <br />
                        <b>Credit Cards Accepted:</b>{" "}
                        {restaurant.credit_cards_accepted ? "Yes" : "No"}
                        <br />
                        <b>Happy Hour:</b> {restaurant.happy_hour ? "Yes" : "No"}
                        <br />
                        <b>Dogs Allowed:</b> {restaurant.dogs_allowed ? "Yes" : "No"}
                        <br />
                        <b>Sustainable:</b> {restaurant.sustainable ? "Yes" : "No"}
                      </Popup>
                    </Marker>
                  ))}
                </MapContainer>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    minHeight: "100vh",
    backgroundColor: "#e0f7fa",
  },
  sidebar: {
    width: "250px",
    backgroundColor: "#ffffff",
    padding: "1rem",
    borderRight: "1px solid #ddd",
  },
  sidebarTitle: {
    fontSize: "1.5rem",
    color: "#0277bd",
    marginBottom: "1rem",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  label: {
    fontSize: "1rem",
    color: "#01579b",
  },
  input: {
    width: "100%",
    padding: "0.3rem 0.5rem",
    borderRadius: "4px",
    border: "1px solid #81d4fa",
    boxSizing: "border-box",
  },
  buttonFilters: {
    display: "flex",
    flexWrap: "wrap",
    gap: "0.5rem",
  },
  filterButton: {
    padding: "0.5rem 1rem",
    fontSize: "0.9rem",
    color: "#ffffff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
  button: {
    padding: "0.75rem",
    backgroundColor: "#0288d1",
    color: "#ffffff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
  mainContent: {
    flex: 1,
    padding: "1rem",
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  toggleButtons: {
    display: "flex",
    gap: "1rem",
    marginBottom: "1rem",
    alignItems: "center",
  },
  toggleButton: {
    padding: "0.5rem 1rem",
    backgroundColor: "#0277bd",
    color: "#ffffff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  results: {
    display: "flex",
    gap: "1rem",
    height: "calc(100vh - 2rem)", // Adjust height to account for the top bar
  },
  tableContainer: {
    flex: 1,
    overflowX: "auto",
  },
  tableTitle: {
    fontSize: "1.5rem",
    color: "#0277bd",
    marginBottom: "1rem",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    textAlign: "left",
  },
  th: {
    backgroundColor: "#0288d1",
    color: "#ffffff",
    padding: "0.5rem",
  },
  td: {
    padding: "0.5rem",
    borderBottom: "1px solid #ddd",
  },
  mapContainer: {
    flex: 1,
    height: "100%",
    borderRadius: "8px",
    overflow: "hidden",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
};

export default RestaurantList;