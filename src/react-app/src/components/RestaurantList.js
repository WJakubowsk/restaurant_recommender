import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIconRetina from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
// Fix Leaflet's default icon issue in React
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIconRetina,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});


const cuisineOptions = [
  "Acai Bowls", "African", "American (New)", "American (Traditional)", "Arabic", 
  "Argentine", "Armenian", "Asian Fusion", "Australian", "Austrian", "Bagels", 
  "Bakeries", "Bangladeshi", "Barbeque", "Bars", "Basque", "Beer", "Beer Bar", 
  "Beer Gardens", "Beer Hall", "Belgian", "Bistros", "Brewpubs", "Breakfast & Brunch", 
  "British", "Bubble Tea", "Buffets", "Burgers", "Burmese", "Cafes", "Cafeteria", 
  "Calabrian", "Cambodian", "Canadian (New)", "Cantonese", "Caribbean", "Caterers", 
  "Cheesesteaks", "Chicken Wings", "Chinese", "Chocolatiers & Shops", "Cocktail Bars", 
  "Coffee & Tea", "Coffee Roasteries", "Coffeeshops", "Colombian", "Comfort Food", 
  "Conveyor Belt Sushi", "Creperies", "Cuban", "Cucina campana", "Cupcakes", "Custom Cakes", 
  "Czech", "Dim Sum", "Diners", "Desserts", "Donburi", "Donuts", "Dominican", "Dumplings", 
  "Eastern European", "Egyptian", "Empanadas", "English", "Ethical Grocery", 
  "Ethnic Food", "Ethnic Grocery", "Ethiopian", "Falafel", "Fast Food", "Filipino", 
  "Fish & Chips", "Fondue", "Food Court", "Food Stands", "Food Trucks", "French", 
  "Fruits & Veggies", "Fuzhou", "Gastropubs", "Georgian", "Gelato", "German", 
  "Gluten-Free", "Greek", "Guamanian", "Hakka", "Halal", "Hainan", "Haitian", 
  "Hawaiian", "Health Markets", "Himalayan/Nepalese", "Hong Kong Style Cafe", 
  "Honduran", "Hot Dogs", "Hot Pot", "Hotel bar", "Hungarian", "Ice Cream & Frozen Yogurt", 
  "Indian", "Indonesian", "International", "Irish", "Irish Pub", "Israeli", "Italian", 
  "Izakaya", "Japanese", "Japanese Curry", "Juice Bars & Smoothies", "Kebab", 
  "Kombucha", "Korean", "Kosher", "Lahmacun", "Latin American", "Laotian", "Lebanese", 
  "Live/Raw Food", "Local Flavor", "Macarons", "Malaysian", "Margaritas", "Mediterranean", 
  "Mexican", "Middle Eastern", "Modern European", "Mongolian", "Moroccan", "Nicaraguan", 
  "Nightlife", "Noodles", "Organic Stores", "Oriental", "Pakistani", "Pan Asian", 
  "Pancakes", "Parent Cafes", "Pasta Shops", "Patisserie/Cake Shop", "Peruvian", 
  "Persian/Iranian", "Pita", "Pizza", "Polish", "Poke", "Pop-Up Restaurants", 
  "Portuguese", "Poutineries", "Pretzels", "Puerto Rican", "Pubs", "Ramen", "Russian", 
  "Salad", "Salvadoran", "Sandwiches", "Sardinian", "Scottish", "Seafood", 
  "Senegalese", "Serbo Croatian", "Shanghainese", "Singaporean", "Sicilian", 
  "Soul Food", "Soup", "Southern", "Specialty Food", "Sports Bars", "Sri Lankan", 
  "Steakhouses", "Sushi Bars", "Szechuan", "Syrian", "Tacos", "Taiwanese", 
  "Tapas Bars", "Tapas/Small Plates", "Tea Rooms", "Teppanyaki", "Tex-Mex", 
  "Thai", "Themed Cafes", "Tiki Bars", "Tonkatsu", "Trinidadian", "Turkish", 
  "Tuscan", "Ukrainian", "Uzbek", "Vegan", "Vegetarian", "Vietnamese", "Venezuelan", 
  "Waffles", "Whiskey Bars", "Wine & Spirits", "Wine Bars", "Wineries", "Wraps"
];

const getCSRFToken = () => {
  const csrfCookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));
  return csrfCookie ? csrfCookie.split("=")[1] : "";
};

const formatFiltersForQuery = (filters) => {
  const formattedFilters = { ...filters };
  Object.keys(formattedFilters).forEach((key) => {
    if (typeof formattedFilters[key] === "boolean") {
      formattedFilters[key] = formattedFilters[key] ? "on" : "";
    }
  });
  return formattedFilters;
};
const formatPriceRange = (priceRange) => {
  const symbols = ["", "$", "$$", "$$$", "$$$$"];
  return symbols[priceRange] || "Unknown";
};



const RestaurantList = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [cuisines, setCuisines] = useState([]);
  const [ambiences, setAmbiences] = useState([]);
  const [filters, setFilters] = useState({
    name: "",
    cuisine: "",
    ambience: "",
    min_rating: "",
    city: "",
    price_range: "",
    open_now: "",
    delivery: "",
    good_for_kids: "",
    good_for_groups: "",
    take_out: "",
    reservations: "",
    outdoor_seating: "",
    wheelchair_accessible: "",
    bike_parking: "",
    credit_cards_accepted: "",
    happy_hour: "",
    dogs_allowed: "",
    sustainable: "",
  });
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [filtersApplied, setFiltersApplied] = useState(false);
  const [showTable, setShowTable] = useState(true);
  const [showMap, setShowMap] = useState(true);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);

  useEffect(() => {
    fetchRestaurants();
    fetchCuisines();
    fetchAmbiences();
  }, []);
  const fetchAmbiences = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/ambiences/");
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setAmbiences(data); // Assuming the backend returns a list of ambiences
    } catch (error) {
        console.error("Error fetching ambiences:", error);
    }
};
  const fetchCuisines = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/cuisines/");
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setCuisines(data); // Assuming the backend returns a list of cuisines
    } catch (error) {
      console.error("Error fetching cuisines:", error);
    }
  };

  const fetchRestaurants = async () => {
    try {
        const queryParams = new URLSearchParams(filters).toString();
        const response = await fetch(`http://127.0.0.1:8000/api/restaurants/?${queryParams}`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setRestaurants(data.restaurants);
    } catch (error) {
        console.error("Error fetching restaurants:", error);
    }
};


  const handleFilterSubmit = (e) => {
    e.preventDefault();
    setFiltersApplied(true);
    fetchRestaurants();
  };

  const toggleButtonFilter = (field) => {
    setFilters((prev) => ({
      ...prev,
      [field]: prev[field] === true ? false : true, // Toggle between "" and true
    }));
  };
  
  

  const handleRowClick = (restaurant) => {
    setSelectedRestaurant(restaurant);
  };

  const MapFocus = ({ position }) => {
    const map = useMap();
    useEffect(() => {
      if (position) {
        map.flyTo(position, 15, { duration: 0.5 });
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
           <select
              name="cuisine"
              value={filters.cuisine}
              onChange={(e) => setFilters({ ...filters, cuisine: e.target.value })}
              style={styles.input}
            >
              <option value="">Select Cuisine</option>
              {cuisines.map((cuisine) => (
                <option key={cuisine.id} value={cuisine.id}>
                  {cuisine.name}
                </option>
              ))}
            </select>


          </label>

          <label style={styles.label}>
            Ambience:
            <select
              name="ambience"
              value={filters.ambience}
              onChange={(e) => setFilters({ ...filters, ambience: e.target.value })}
              style={styles.input}
          >
              <option value="">Select Ambience</option>
              {ambiences.map((ambience) => (
                  <option key={ambience.id} value={ambience.id}>
                      {ambience.name}
                  </option>
              ))}
          </select>
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
              min="1" // Minimum value
              max="5" // Maximum value
              step="0.5" // Increment step
              placeholder="Enter a rating (1-5)"
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
          <select
            name="price_range"
            value={filters.price_range}
            onChange={(e) =>
              setFilters({ ...filters, price_range: e.target.value })
            }
            style={styles.input}
          >
            <option value="">Select</option>
            <option value="1">$</option>
            <option value="2">$$</option>
            <option value="3">$$$</option>
            <option value="4">$$$$</option>
          </select>
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
                  </tr>
                </thead>
                <tbody>
                  {restaurants.map((restaurant, index) => (
                    <tr key={index} onClick={() => handleRowClick(restaurant)}>
                      <td style={styles.td}>{restaurant.name}</td>
                      <td style={styles.td}>{restaurant.cuisine.join(", ")}</td>
                      <td style={styles.td}>{restaurant.city}</td>
                      <td style={styles.tdCentered}>{restaurant.rating}</td>
                      <td style={styles.tdCentered}>{formatPriceRange(restaurant.price_range)}</td>
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
                      selectedRestaurant.longitude,
                    ]}
                  />
                )}
                                {restaurants.map((restaurant, index) => (
                    <Marker
                        
                        position={[restaurant.latitude, restaurant.longitude]}
                    >
                        <Popup>
                          <b>{restaurant.name}</b>
                          <br />
                          <b>Cuisine:</b> {restaurant.cuisine.join(", ")}
                          <br />
                          <b>Ambience:</b> {restaurant.ambience.join(", ")}
                          <br />
                          <b>City:</b> {restaurant.city}
                          <br />
                          <b>Rating:</b> {restaurant.rating} stars
                          <br />
                          <b>Price Range:</b> {formatPriceRange(restaurant.price_range)}
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
                          <b>Outdoor Seating:</b> {restaurant.outdoor_seating ? "Yes" : "No"}
                          <br />
                          <b>Wheelchair Accessible:</b> {restaurant.wheelchair_accessible ? "Yes" : "No"}
                          <br />
                          <b>Bike Parking:</b> {restaurant.bike_parking ? "Yes" : "No"}
                          <br />
                          <b>Credit Cards Accepted:</b> {restaurant.credit_cards_accepted ? "Yes" : "No"}
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
table: {
  width: "100%",
  borderCollapse: "collapse", // Ensure the borders don't overlap
  textAlign: "left",
},
th: {
  backgroundColor: "#0288d1",
  color: "#ffffff",
  padding: "0.5rem",
  border: "1px solid #ddd", // Add border to header cells
},
td: {
  padding: "0.5rem",
  border: "1px solid #ddd", // Add border to table cells
},
tdCentered: {
  padding: "0.5rem",
  border: "1px solid #ddd",
  textAlign: "center", // Center the content for specific cells
},
};

export default RestaurantList;
