import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = ({ onLogin }) => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.token); // Save token for authenticated requests
        onLogin(); // Trigger login state in parent
        navigate("/"); // Redirect to home or another page
      } else {
        const data = await response.json();
        setError(data.error || "Login failed");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
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
      {/* Large header text */}
      <h1
        style={{
          fontSize: "48px",
          color: "#0277bd",
          marginBottom: "30px",
          textAlign: "center",
          fontWeight: "bold",
        }}
      >
        Restaurant Recommender
      </h1>

      {/* Login panel */}
      <div
        style={{
          background: "white",
          padding: "30px 40px",
          borderRadius: "10px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
          width: "100%",
          maxWidth: "400px",
        }}
      >
        <h2
          style={{
            fontSize: "24px",
            marginBottom: "20px",
            textAlign: "center",
            color: "#0277bd",
          }}
        >
          Login
        </h2>
        {error && (
          <p
            style={{
              color: "red",
              fontSize: "14px",
              marginBottom: "15px",
              textAlign: "center",
            }}
          >
            {error}
          </p>
        )}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "15px" }}>
            <label
              htmlFor="username"
              style={{
                display: "block",
                fontWeight: "bold",
                marginBottom: "5px",
                color: "#01579b",
              }}
            >
              Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              style={{
                width: "100%",
                padding: "10px",
                border: "1px solid #81d4fa",
                borderRadius: "5px",
                fontSize: "14px",
                boxSizing: "border-box",
              }}
            />
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label
              htmlFor="password"
              style={{
                display: "block",
                fontWeight: "bold",
                marginBottom: "5px",
                color: "#01579b",
              }}
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              style={{
                width: "100%",
                padding: "10px",
                border: "1px solid #81d4fa",
                borderRadius: "5px",
                fontSize: "14px",
                boxSizing: "border-box",
              }}
            />
          </div>

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: "#0277bd",
              color: "white",
              fontSize: "16px",
              fontWeight: "bold",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              transition: "background-color 0.3s",
            }}
            onMouseOver={(e) =>
              (e.target.style.backgroundColor = "#01579b")
            }
            onMouseOut={(e) =>
              (e.target.style.backgroundColor = "#0277bd")
            }
          >
            Login
          </button>
        </form>
        <p
          style={{
            marginTop: "15px",
            textAlign: "center",
            fontSize: "14px",
          }}
        >
          Don't have an account?{" "}
          <span
            style={{ color: "#0277bd", cursor: "pointer", fontWeight: "bold" }}
            onClick={() => navigate("/signup")}
          >
            Sign up here
          </span>
        </p>
      </div>
    </div>
  );
};

export default Login;

