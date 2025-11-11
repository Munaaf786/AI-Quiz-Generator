import React from "react";

function QuizDisplay({ quizData }) {
  if (!quizData) {
    return (
      <div className="p-8 text-center text-gray-500 dark:text-gray-400">
        No quiz data to display. Generate a quiz first!
      </div>
    );
  }

  const { title, summary, key_entities, sections, quiz, related_topics } =
    quizData;

  const getOptionLetter = (index) => String.fromCharCode(65 + index); // A, B, C, D
  let optionLetter;

  return (
    <div className="space-y-8 p-6 bg-white dark:bg-gray-900 rounded-lg shadow-md">
      {/* Article Title and Summary */}
      <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg shadow-inner">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {title}
        </h3>
        {summary && (
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {summary}
          </p>
        )}

        {/* Key Entities */}
        {(key_entities?.people?.length > 0 ||
          key_entities?.organizations?.length > 0 ||
          key_entities?.locations?.length > 0) && (
          <div className="mt-4 text-gray-700 dark:text-gray-300 text-sm">
            {key_entities.people?.length > 0 && (
              <p className="mb-1">
                <span className="font-semibold">People:</span>{" "}
                {key_entities.people.join(", ")}
              </p>
            )}
            {key_entities.organizations?.length > 0 && (
              <p className="mb-1">
                <span className="font-semibold">Organizations:</span>{" "}
                {key_entities.organizations.join(", ")}
              </p>
            )}
            {key_entities.locations?.length > 0 && (
              <p>
                <span className="font-semibold">Locations:</span>{" "}
                {key_entities.locations.join(", ")}
              </p>
            )}
          </div>
        )}

        {/* Sections */}
        {sections?.length > 0 && (
          <div className="mt-4 text-gray-700 dark:text-gray-300 text-sm">
            <span className="font-semibold">Sections:</span>{" "}
            {sections.join(", ")}
          </div>
        )}
      </div>

      {/* Quiz Questions */}
      <div className="space-y-6">
        {quiz?.map((q, qIndex) => (
          <div
            key={qIndex}
            className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg shadow-inner border border-gray-200 dark:border-gray-700"
          >
            <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Question {qIndex + 1}: {q.question}
            </h4>
            <div className="space-y-3">
              {q.options.map((option, oIndex) => {
                const isCorrect = option === q.answer;
                if (isCorrect) {
                  optionLetter = getOptionLetter(oIndex);
                }
                return (
                  <div
                    key={oIndex}
                    className={`p-3 rounded-md border text-gray-800 dark:text-gray-200
                                ${
                                  isCorrect
                                    ? "border-indigo-500 bg-indigo-50 dark:bg-indigo-950" // Correct answer highlight
                                    : "border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
                                }
                                transition-all duration-200`}
                  >
                    <span className="font-medium mr-2">
                      {getOptionLetter(oIndex)}.
                    </span>
                    {option}
                  </div>
                );
              })}
            </div>
            <div className="mt-4 flex flex-col sm:flex-row sm:items-center justify-between text-sm">
              <p className="text-gray-700 dark:text-gray-300">
                <span className="font-semibold">Correct Answer:</span>{" "}
                <span className="text-indigo-600 dark:text-indigo-400 font-medium">
                  {optionLetter}
                  {`) ${q.answer}`}
                </span>
              </p>
              <span
                className="mt-2 w-fit sm:mt-0 px-3 py-2 bg-gray-200 dark:bg-gray-700 rounded-full text-xs font-semibold
                               text-gray-700 dark:text-gray-300 capitalize"
              >
                {q.difficulty || "medium"}
              </span>
            </div>
            {q.explanation && (
              <p className="mt-2 text-gray-600 dark:text-gray-400 text-sm">
                <span className="font-semibold">Explanation:</span>{" "}
                {q.explanation}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Related Topics */}
      {related_topics?.length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg shadow-inner">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Related Topics
          </h4>
          <div className="flex flex-wrap gap-2">
            {related_topics.map((topic, index) => (
              <a
                key={index}
                href={`https://en.wikipedia.org/wiki/${encodeURIComponent(
                  topic
                )}`}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-indigo-100 dark:bg-indigo-800 text-indigo-800 dark:text-indigo-200
                           rounded-full text-sm font-medium"
              >
                {topic}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default QuizDisplay;
