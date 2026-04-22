import { motion } from "framer-motion";

export default function Hero() {
  return (
    <div className="bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white py-20 px-6 text-center">
      
      <motion.h2
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl md:text-5xl font-extrabold mb-4"
      >
        Buy, Sell & Donate Books 📚
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="text-gray-400 max-w-xl mx-auto"
      >
        Give your old books a new life. Connect with readers, share knowledge, and build a smarter community.
      </motion.p>

      <motion.button
        whileHover={{ scale: 1.1 }}
        className="mt-6 bg-green-500 hover:bg-green-600 px-6 py-3 rounded-xl font-semibold shadow-lg transition"
      >
        Get Started 🚀
      </motion.button>
    </div>
  );
}