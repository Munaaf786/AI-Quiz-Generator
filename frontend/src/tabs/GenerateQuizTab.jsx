// frontend/src/tabs/GenerateQuizTab.jsx
import React, { useState, useEffect } from "react";
import { generateQuiz, getArticleTitlePreview } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";
import QuizDisplay from "../components/QuizDisplay";

function GenerateQuizTab() {
  const [url, setUrl] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [previewTitle, setPreviewTitle] = useState("");
  const [debouncedUrl, setDebouncedUrl] = useState("");

  // Debounce URL input for title preview
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedUrl(url);
    }, 500); // 500ms debounce
    return () => {
      clearTimeout(handler);
    };
  }, [url]);

  // Fetch preview title when debouncedUrl changes
  useEffect(() => {
    const fetchTitle = async () => {
      if (
        debouncedUrl &&
        debouncedUrl.startsWith("https://en.wikipedia.org/wiki/")
      ) {
        setPreviewTitle("Fetching title...");
        setError(null);
        try {
          const title = await getArticleTitlePreview(debouncedUrl);
          setPreviewTitle(title || "Could not fetch title.");
        } catch (err) {
          console.error("Failed to fetch preview title:", err);
          setPreviewTitle("Error fetching title.");
        }
      } else if (debouncedUrl) {
        setPreviewTitle("Invalid Wikipedia URL.");
      } else {
        setPreviewTitle("");
      }
    };
    fetchTitle();
  }, [debouncedUrl]);

  const handleGenerateQuiz = async () => {
    setError(null);
    setQuizData(null);
    if (!url.startsWith("https://en.wikipedia.org/wiki/")) {
      setError("Please enter a valid Wikipedia article URL.");
      return;
    }

    setLoading(true);
    try {
      const data = await generateQuiz(url);
      setQuizData(data);
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
          Enter Wikipedia Article URL
        </h2>
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            className="flex-grow p-3 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                       bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
            placeholder="https://en.wikipedia.org/wiki/..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button
            onClick={handleGenerateQuiz}
            className="px-6 py-3 bg-gradient-to-r from-sky-400 to-violet-500 
hover:from-sky-500 hover:to-violet-600 
text-white font-semibold rounded-md shadow-sm 
focus:outline-none focus:ring-2 focus:ring-sky-400 focus:ring-offset-2 
dark:focus:ring-offset-gray-900 transition-colors duration-200 cursor-pointer"
            disabled={
              loading || !url.startsWith("https://en.wikipedia.org/wiki/")
            }
          >
            Generate Quiz
          </button>
        </div>
        {previewTitle && (
          <p className="mt-3 text-md text-gray-600 dark:text-gray-300 italic">
            Title: {previewTitle}
          </p>
        )}
        {error && (
          <p className="mt-4 text-red-500 dark:text-red-400">{error}</p>
        )}
      </div>

      {loading && <LoadingSpinner isGenerateTab={true} />}

      {quizData && !loading && (
        <QuizDisplay quizData={quizData} /> // Pass quizData to QuizDisplay
      )}

      {!quizData && !loading && !error && (
        <div className="p-8 text-center text-gray-500 dark:text-gray-400">
          Enter a Wikipedia URL above to generate a quiz!
        </div>
      )}
    </div>
  );
}

export default GenerateQuizTab;
