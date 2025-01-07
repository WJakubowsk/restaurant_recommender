import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import the useNavigate hook

const Signup = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const navigate = useNavigate(); // Initialize the useNavigate hook

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Sign up data submitted:", formData);

    // Add your sign-up logic here (e.g., API request)
    // Simulate successful signup
    setTimeout(() => {
      console.log("Sign up successful!");
      navigate("/"); // Navigate to the restaurant list page
    }, 500); // Mocking a slight delay
  };

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <h1 style={styles.title}>Sign Up</h1>
        <p style={styles.subtitle}>Create an account to start discovering restaurants</p>

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              style={styles.input}
              placeholder="Enter your name"
              required
            />
          </label>

          <label style={styles.label}>
            Email:
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              style={styles.input}
              placeholder="Enter your email"
              required
            />
          </label>

          <label style={styles.label}>
            Password:
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              style={styles.input}
              placeholder="Enter your password"
              required
            />
          </label>

          <label style={styles.label}>
            Confirm Password:
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              style={styles.input}
              placeholder="Confirm your password"
              required
            />
          </label>

          <button type="submit" style={styles.button}>
            Sign Up
          </button>
        </form>

        <p style={styles.linkText}>
          Already have an account? <a href="/login" style={styles.link}>Log in here</a>.
        </p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    backgroundColor: "#e0f7fa",
  },
  content: {
    width: "100%",
    maxWidth: "400px",
    backgroundColor: "#ffffff",
    padding: "2rem",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  title: {
    fontSize: "2rem",
    color: "#0277bd",
    textAlign: "center",
    marginBottom: "1rem",
  },
  subtitle: {
    fontSize: "1rem",
    color: "#01579b",
    textAlign: "center",
    marginBottom: "2rem",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  label: {
    fontSize: "1rem",
    color: "#01579b",
    fontWeight: "bold",
  },
  input: {
    width: "100%",
    padding: "0.5rem",
    fontSize: "1rem",
    borderRadius: "4px",
    border: "1px solid #81d4fa",
    boxSizing: "border-box",
  },
  button: {
    padding: "0.75rem",
    fontSize: "1rem",
    color: "#ffffff",
    backgroundColor: "#0288d1",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    textAlign: "center",
    transition: "background-color 0.3s",
  },
  linkText: {
    marginTop: "1rem",
    textAlign: "center",
    color: "#01579b",
  },
  link: {
    color: "#0288d1",
    textDecoration: "none",
    fontWeight: "bold",
  },
};

export default Signup;
