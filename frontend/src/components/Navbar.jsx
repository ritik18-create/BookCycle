import { useState } from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="bg-black/80 backdrop-blur-md text-white px-6 py-4 shadow-lg sticky top-0 z-50">
      <div className="flex justify-between items-center">
        
        {/* Logo */}
        <h1 className="text-2xl font-bold text-green-400 tracking-wide">
          📚 BookCycle
        </h1>

        {/* Desktop Menu */}
        <div className="hidden md:flex gap-6 font-medium">
          <Link to="/" className="hover:text-green-400 transition">Home</Link>
          <Link to="/dashboard" className="hover:text-green-400 transition">Dashboard</Link>
          <Link to="/login" className="hover:text-green-400 transition">Login</Link>
        </div>

        {/* Mobile Toggle */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden text-xl"
        >
          ☰
        </button>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="flex flex-col mt-4 gap-3 md:hidden">
          <Link to="/" className="hover:text-green-400">Home</Link>
          <Link to="/dashboard" className="hover:text-green-400">Dashboard</Link>
          <Link to="/login" className="hover:text-green-400">Login</Link>
        </div>
      )}
    </nav>
  );
}