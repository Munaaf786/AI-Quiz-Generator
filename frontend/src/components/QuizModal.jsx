import React from "react";
import { HiMiniXMark } from "react-icons/hi2";

function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900 bg-opacity-75 dark:bg-opacity-85 transition-opacity duration-300">
      <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 transition-transform duration-300 scale-100 opacity-100">
        <div className="flex justify-between items-center pb-4 border-b border-gray-200 dark:border-gray-700 mb-4">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
            {title || "Details"}
          </h3>
          <button
            onClick={onClose}
            className="p-1 rounded-full text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Close modal"
          >
            <HiMiniXMark className="h-6 w-6" />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

export default Modal;
