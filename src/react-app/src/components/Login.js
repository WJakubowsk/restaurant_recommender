import React from "react";
import { useNavigate } from "react-router-dom";

const Login = ({ onLogin }) => {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("User logged in");
    onLogin();
    navigate("/");
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h1 style={styles.title}>Welcome Back</h1>
        <p style={styles.subtitle}>Log in to access the best restaurants</p>
        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>
            Username:
            <input type="text" name="username" required style={styles.input} />
          </label>
          <label style={styles.label}>
            Password:
            <input type="password" name="password" required style={styles.input} />
          </label>
          <button type="submit" style={styles.button}>
            Login
          </button>
        </form>
        <p style={styles.footerText}>
          Don't have an account?{" "}
          <a href="/signup" style={styles.link}>
            Sign up here
          </a>.
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
    height: "100vh",
    backgroundColor: "#e0f7fa", // Light blue background
    margin: 0,
  },
  formContainer: {
    backgroundColor: "#ffffff", // White form background
    padding: "2rem",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    width: "90%",
    maxWidth: "400px",
    textAlign: "center",
  },
  title: {
    fontSize: "2rem",
    color: "#0277bd", // Deep blue color
    margin: "0 0 0.5rem",
  },
  subtitle: {
    fontSize: "1rem",
    color: "#01579b", // Slightly darker blue
    marginBottom: "1.5rem",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  label: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    fontSize: "1rem",
    color: "#01579b",
    fontWeight: "bold",
  },
  input: {
    width: "100%",
    padding: "0.5rem",
    fontSize: "1rem",
    borderRadius: "4px",
    border: "1px solid #81d4fa", // Light blue border
    outline: "none",
    marginTop: "0.25rem",
  },
  inputFocus: {
    borderColor: "#0277bd", // Focused border
  },
  button: {
    padding: "0.75rem",
    fontSize: "1rem",
    color: "#ffffff",
    backgroundColor: "#0288d1", // Primary blue
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
  buttonHover: {
    backgroundColor: "#01579b", // Darker blue on hover
  },
  footerText: {
    fontSize: "0.9rem",
    color: "#01579b",
    marginTop: "1rem",
  },
  link: {
    color: "#0288d1",
    textDecoration: "none",
    fontWeight: "bold",
  },
};

export default Login;
