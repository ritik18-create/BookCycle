import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import API from "../services/api";
import AddBook from "../components/AddBook";
import { jwtDecode } from "jwt-decode";

function Dashboard() {
  const token = localStorage.getItem("token");
  const user = token ? jwtDecode(token) : null;

  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [showForm, setShowForm] = useState(false);

  // ✅ NEW STATES
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // 🔐 Protect route
  useEffect(() => {
    if (!token) {
      navigate("/");
    }
  }, []);

  // 📚 Fetch books
  const fetchBooks = async () => {
    try {
      setLoading(true);
      const res = await API.get("/books/");
      setBooks(res.data);
      setError("");
    } catch (err) {
      setError("Failed to load books");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  // ❌ Delete book

  const deleteBook = async (id) => {
  const confirmDelete = window.confirm("Are you sure?");
  if (!confirmDelete) return;

  try {
    await API.delete(`/books/delete/${id}/`);
    fetchBooks();
  } catch (err) {
    alert("Delete failed");
  }
};

  // 🛒 Buy book
  const buyBook = async (id) => {
    try {
      await API.post(`/books/buy/${id}/`);
      fetchBooks();
    } catch (err) {
      alert(err.response?.data?.error || "Buy failed");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-6">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
            📚 BookCycle Dashboard
          </h1>
          <p className="text-gray-400 mt-1">
            Manage your books, explore listings, and contribute ♻️
          </p>
        </div>

        {/* Buttons */}
        <div className="flex gap-3 mt-4 md:mt-0">
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded-lg text-sm font-medium shadow-md transition"
          >
            {showForm ? "Close" : "+ Add Book"}
          </button>

          <button
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/";
            }}
            className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg text-sm font-medium shadow-md transition"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Add Book Form */}
      {showForm && (
        <AddBook
          onBookAdded={() => {
            fetchBooks();
            setShowForm(false);
          }}
        />
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
        {[
          { title: "Books Listed", value: books.length },
          { title: "Books Sold", value: books.filter(b => b.status === "sold").length },
          { title: "Donations", value: books.filter(b => b.type === "donate").length },
        ].map((item, i) => (
          <motion.div
            key={i}
            whileHover={{ scale: 1.05 }}
            className="bg-white/10 backdrop-blur-md p-6 rounded-2xl shadow-lg border border-white/10"
          >
            <h2 className="text-lg text-gray-300">{item.title}</h2>
            <p className="text-2xl font-bold mt-2">{item.value}</p>
          </motion.div>
        ))}
      </div>

      {/* Books Section */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">📖 Your Books</h2>

        {/* ✅ Loading */}
        {loading && (
          <p className="text-blue-400 text-center">Loading books...</p>
        )}

        {/* ❌ Error */}
        {error && (
          <p className="text-red-400 text-center">{error}</p>
        )}

        {/* 🚫 Empty */}
        {!loading && !error && books.length === 0 && (
          <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/10 text-center">
            <p className="text-gray-400">
              No books available 🚫
            </p>
          </div>
        )}

        {/* ✅ Books Grid */}
        {!loading && !error && books.length > 0 && (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {books.map((book) => (
              <motion.div
                key={book.id}
                whileHover={{ scale: 1.03 }}
                className="bg-white/10 backdrop-blur-md p-5 rounded-2xl shadow-lg border border-white/10 flex flex-col justify-between"
              >
                {/* Image */}
                {book.image && (
                  <img
                    src={book.image}
                    alt={book.title}
                    className="w-full h-40 object-cover rounded-lg mb-3"
                  />
                )}

                {/* Content */}
                <div>
                  <h3 className="text-xl font-bold">{book.title}</h3>
                  <p className="text-sm text-gray-400">{book.author}</p>

                  <p className="text-blue-400 font-semibold mt-2">
                    {book.type.toUpperCase()}
                  </p>

                  {book.type === "sell" && (
                    <p className="text-green-400 font-semibold mt-1">
                      ₹{book.price}
                    </p>
                  )}

                  {book.type === "buy" && (
                    <p className="text-orange-400 mt-1 font-medium">
                      Looking to Buy
                    </p>
                  )}

                  {book.type === "donate" && (
                    <p className="text-purple-400 mt-1 font-medium">
                      Free Donation 🎁
                    </p>
                  )}

                  {book.status === "sold" && (
                    <p className="text-red-400 font-semibold mt-2">
                      Sold ❌
                    </p>
                  )}
                </div>

                {/* Actions */}
                <div className="mt-4 flex gap-2">
                  {book.type === "sell" &&
                    book.status === "available" &&
                    user &&
                    user.user_id !== book.user_id && (
                      <button
                         onClick={() => buyBook(book.id)}
//                         onClick={async ()=>{

//    const res = await buyBook(book._id);

//    alert(res.message);

//  }}
                        className="flex-1 bg-green-500 hover:bg-green-600 py-2 rounded-lg text-sm font-semibold transition"
                      >
                        Buy
                      </button>
                    )}

                  {user && user.user_id === book.user_id && (
                    <button
                      onClick={() => deleteBook(book.id)}
                      className="flex-1 bg-red-500 hover:bg-red-600 py-2 rounded-lg text-sm font-semibold transition"
                    >
                      Delete
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;