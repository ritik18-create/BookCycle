import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";

function Login() {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

const navigate = useNavigate();

const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const res = await API.post("/auth/login/", form);

    // Save token
    localStorage.setItem("token", res.data.token);

    // Redirect
    navigate("/dashboard");
  } catch (err) {
    alert(err.response?.data?.error || "Login failed");
  }
};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 px-4">
      
      {/* Glass Card */}
      <form
        onSubmit={handleSubmit}
        className="backdrop-blur-lg bg-white/10 border border-white/20 shadow-2xl rounded-2xl p-8 w-full max-w-md text-white transition-all duration-300 hover:scale-[1.02]"
      >
        {/* Title */}
        <h2 className="text-3xl font-extrabold text-center mb-6 tracking-wide">
          Welcome Back 👋
        </h2>

        <p className="text-center text-sm text-white/80 mb-6">
          Login to your BookCycle account
        </p>

        {/* Email */}
        <div className="mb-4">
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
          />
        </div>

        {/* Password */}
        <div className="mb-4">
          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
          />
        </div>

        {/* Forgot */}
        <div className="flex justify-end text-sm mb-4">
          <span className="cursor-pointer text-white/80 hover:text-white transition">
            Forgot password?
          </span>
        </div>

        {/* Button */}
        <button
          className="w-full py-3 rounded-lg bg-white text-indigo-600 font-semibold hover:bg-indigo-100 transition duration-300 shadow-lg"
        >
          Login
        </button>

        {/* Divider */}
        <div className="my-6 flex items-center gap-2">
          <div className="flex-1 h-px bg-white/30"></div>
          <span className="text-sm text-white/70">OR</span>
          <div className="flex-1 h-px bg-white/30"></div>
        </div>

        {/* Signup */}
        <p className="text-center text-sm text-white/80">
          Don’t have an account?{" "}
          <span className="font-semibold cursor-pointer hover:text-white transition">
            Sign up
          </span>
        </p>
      </form>
    </div>
  );
}

export default Login;