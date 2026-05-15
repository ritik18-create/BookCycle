import axios from "axios";

// Axios instance
const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Automatically attach JWT token
API.interceptors.request.use(
  (req) => {
    const token = localStorage.getItem("token");

    if (token) {
      req.headers.Authorization = `Bearer ${token}`;
    }

    console.log("TOKEN SENT:", token);

    return req;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ================= AUTH APIs =================

// REGISTER USER
export const registerUser = async (data) => {
  const response = await fetch(
    "http://127.0.0.1:8000/api/auth/register/",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );

  return response.json();
};

// LOGIN USER
export const loginUser = async (data) => {
  const response = await fetch(
    "http://127.0.0.1:8000/api/auth/login/",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );

  return response.json();
};

// ================= USER APIs =================

// Protected Route Example
export const getProfile = async () => {
  return await API.get("/profile/");
};

// Logout User
export const logoutUser = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("refresh");
};

export default API;