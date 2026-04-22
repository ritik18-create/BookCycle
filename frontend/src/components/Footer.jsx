export default function Footer() {
  return (
    <footer className="bg-black text-gray-400 text-center py-6 mt-10 border-t border-gray-800">
      <p className="text-sm">
        © {new Date().getFullYear()} BookCycle. All rights reserved.
      </p>

      <div className="mt-2 flex justify-center gap-6 text-sm">
        <span className="hover:text-white cursor-pointer">Privacy</span>
        <span className="hover:text-white cursor-pointer">Terms</span>
        <span className="hover:text-white cursor-pointer">Contact</span>
      </div>
    </footer>
  );
}