import { useState } from "react";
import { motion } from "framer-motion";
import API from "../services/api";

function AddBook({ onBookAdded }) {
  const [form, setForm] = useState({
    title: "",
    author: "",
    price: "",
    image: "",
    type: "sell",
  });

  const [loading, setLoading] = useState(false); // ✅ NEW

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // ✅ Basic validation (prevents empty submission bug)
    if (!form.title || !form.author || !form.type) {
      alert("Please fill required fields");
      return;
    }

    setLoading(true);

    try {
      await API.post("/books/add/", form);

      onBookAdded();

      setForm({
        title: "",
        author: "",
        price: "",
        image: "",
        type: "sell",
      });
    } catch (err) {
      console.error(err);
      alert("Failed to add book");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/10 backdrop-blur-md border border-white/20 shadow-2xl rounded-2xl p-6 mb-8 text-white w-full max-w-xl mx-auto"
    >
      {/* Title */}
      <h2 className="text-2xl font-bold mb-4 text-center tracking-wide">
        📚 Add New Book
      </h2>

      <p className="text-center text-sm text-white/70 mb-6">
        Share your books with the community
      </p>

      {/* Title */}
      <div className="mb-4">
        <input
          name="title"
          placeholder="Book Title"
          value={form.title}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
        />
      </div>

      {/* Author */}
      <div className="mb-4">
        <input
          name="author"
          placeholder="Author Name"
          value={form.author}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
        />
      </div>

      {/* Price */}
      <div className="mb-4">
        <input
          name="price"
          placeholder="Price (₹)"
          value={form.price}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
        />
      </div>

      {/* Image */}
      <div className="mb-4">
        <input
          name="image"
          placeholder="Image URL"
          value={form.image}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-lg bg-white/20 placeholder-white/70 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
        />
      </div>

      {/* Type */}
      <div className="mb-5">
        <select
          name="type"
          value={form.type}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-lg bg-white/20 text-white outline-none border border-transparent focus:border-white focus:ring-2 focus:ring-white/40 transition"
        >
          <option value="sell" className="text-black">Sell</option>
          <option value="buy" className="text-black">Buy</option>
          <option value="donate" className="text-black">Donate</option>
        </select>
      </div>

      {/* Button */}
      <motion.button
        whileTap={{ scale: 0.95 }}
        whileHover={{ scale: 1.02 }}
        disabled={loading} // ✅ disables button
        className={`w-full py-3 rounded-lg font-semibold shadow-lg transition ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-gradient-to-r from-green-400 to-emerald-500 hover:from-green-500 hover:to-emerald-600"
        }`}
      >
        {loading ? "Adding..." : "Add Book 🚀"} {/* ✅ dynamic text */}
      </motion.button>
    </motion.form>
  );
}

export default AddBook;