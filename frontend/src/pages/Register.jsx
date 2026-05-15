import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
function Register() {
  const [form, setForm] = useState({
     username: "",
      email: "",
      password: ""
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
console.log("FORM DATA:", form);
  try {
    const res = await API.post("/auth/register/", form);

    localStorage.setItem("token", res.data.token);

    navigate("/dashboard");
  } catch (err) {
    alert(err.response?.data?.error || "Register failed");
  }
};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-400 via-emerald-500 to-teal-600 px-4">
      
      {/* Glass Card */}
      <form
        onSubmit={handleSubmit}
        className="backdrop-blur-lg bg-white/10 border border-white/20 shadow-2xl rounded-2xl p-8 w-full max-w-md text-white transition-all duration-300 hover:scale-[1.02]"
      >
        {/* Title */}
        <h2 className="text-3xl font-extrabold text-center mb-6 tracking-wide">
          Create Account 🚀
        </h2>

        <p className="text-center text-sm text-white/80 mb-6">
          Join BookCycle and start sharing books
        </p>

        {/* Name */}
        <div className="mb-4">
          <input
            name="username"
            placeholder="Full Name"
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
          />
        </div>

        {/* Email */}
        <div className="mb-4">
          <input
            name="email"
            placeholder="Email Address"
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
          />
        </div>

        {/* Password */}
        <div className="mb-4">
          <input
            type="password"
            name="password"
            placeholder="Create Password"
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
          />
        </div>

        {/* Button */}
        <button
          className="w-full py-3 rounded-lg bg-white text-green-600 font-semibold hover:bg-green-100 transition duration-300 shadow-lg"
        >
          Register
        </button>

        {/* Divider */}
        <div className="my-6 flex items-center gap-2">
          <div className="flex-1 h-px bg-white/30"></div>
          <span className="text-sm text-white/70">OR</span>
          <div className="flex-1 h-px bg-white/30"></div>
        </div>

        {/* Login redirect */}
        <p className="text-center text-sm text-white/80">
          Already have an account?{" "}
          <span className="font-semibold cursor-pointer hover:text-white transition">
            Login
          </span>
        </p>
      </form>
    </div>
  );
}

export default Register;