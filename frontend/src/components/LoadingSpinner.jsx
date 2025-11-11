function LoadingSpinner({ isGenerateTab }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-gray-700 dark:text-gray-300">
      <div
        className="animate-spin inline-block w-8 h-8 border-4 rounded-full border-t-indigo-600 dark:border-t-indigo-400 border-gray-200 dark:border-gray-700"
        role="status"
      >
        <span className="sr-only">Loading...</span>
      </div>
      <p className="mt-4 text-lg">
        {isGenerateTab ? "Generating quiz..." : "Fetching the Past Quizzes"}
      </p>
    </div>
  );
}

export default LoadingSpinner;
