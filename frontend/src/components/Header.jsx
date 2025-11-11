import React from "react";
import { BsSun, BsMoon } from "react-icons/bs";

function Header({ theme, toggleTheme, activeTab, setActiveTab }) {
  const tabClasses = (tabName) =>
    `px-4 py-2 text-center text-lg font-medium cursor-pointer relative transition-all duration-200 ` +
    (activeTab === tabName
      ? `text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-violet-500 dark:from-sky-300 dark:to-violet-400 after:absolute after:bottom-0 after:left-0 
      after:w-full after:h-0.5 after:bg-gradient-to-r after:from-sky-400 after:to-violet-500 dark:after:from-sky-300 dark:after:to-violet-400`
      : `text-gray-600 dark:text-gray-400 hover:text-indigo-400 dark:hover:text-indigo-400`);

  return (
    <header className="container w-full flex flex-col items-center py-4 px-8 my-4 bg-white dark:bg-gray-900 shadow-md rounded-lg transition-colors duration-300">
      <div className="w-full flex flex-col md:flex-row justify-between items-center">
        <div className="w-full md:w-auto flex justify-between items-center md:flex-row flex-row px-2 md:px-0 mb-4 md:mb-0">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-violet-500 bg-clip-text text-transparent">
            Quizipedia
          </h1>
          <button
            onClick={() => {
              toggleTheme();
            }}
            className="p-2 rounded-full flex md:hidden focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-colors duration-200
                      text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
            aria-label="Toggle dark mode"
          >
            {theme === "dark" ? (
              <BsSun className="h-6 w-6" />
            ) : (
              <BsMoon className="h-6 w-6" />
            )}
          </button>
        </div>
        {/* Tab Navigation */}
        <nav className="w-full flex justify-center border-gray-200 dark:border-gray-700">
          {" "}
          {/* Changed to justify-start based on image */}
          <div
            className={tabClasses("generate")}
            onClick={() => setActiveTab("generate")}
          >
            Generate Quiz
          </div>
          <div
            className={tabClasses("history")}
            onClick={() => setActiveTab("history")}
          >
            Past Quizzes (History)
          </div>
        </nav>
        {/* Dark Mode Toggle - now an icon */}
        <button
          onClick={() => {
            toggleTheme();
          }}
          className="p-2 rounded-full hidden md:flex focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-colors duration-200
                     text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
          aria-label="Toggle dark mode"
        >
          {theme === "dark" ? (
            <BsSun className="h-6 w-6" />
          ) : (
            <BsMoon className="h-6 w-6" />
          )}
        </button>
      </div>
    </header>
  );
}

export default Header;
