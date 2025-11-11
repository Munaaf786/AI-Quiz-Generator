// frontend/src/App.jsx
import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import GenerateQuizTab from "./tabs/GenerateQuizTab";
import HistoryTab from "./tabs/HistoryTab";

function App() {
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)')
      .matches
  const [theme, setTheme] = useState(localStorage.getItem("theme") || (prefersDarkMode ? "dark" : "light"));
  const [activeTab, setActiveTab] = useState("generate"); 

  useEffect(() => {
    const htmlElement = document.documentElement;
    if (theme === "dark") {
      htmlElement.classList.add("dark");
    } else {
      htmlElement.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  return (
    <div className="min-h-screen mx-auto flex flex-col items-center p-4 bg-gray-50 dark:bg-gray-800 transition-colors duration-300">
      {/* Header component: Contains title, dark mode toggle, and tab navigation */}
      <Header
        theme={theme}
        toggleTheme={toggleTheme}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Main content area, conditionally rendering the active tab component */}
      <main className="container mx-auto my-8 flex-grow p-6 bg-white dark:bg-gray-900 shadow-lg rounded-lg text-gray-900 dark:text-gray-100 transition-colors duration-300">
        {activeTab === "generate" ? <GenerateQuizTab /> : <HistoryTab />}
      </main>
    </div>
  );
}

export default App;
