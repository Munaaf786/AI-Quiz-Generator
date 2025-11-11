const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const generateQuiz = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate_quiz`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to generate quiz");
    }
    return await response.json();
  } catch (error) {
    console.error("Error generating quiz:", error);
    throw error;
  }
};

export const getQuizHistory = async () => {
  const response = await fetch(`${API_BASE_URL}/history`);

  if (!response.ok) {
    throw new Error("Failed to fetch quiz history");
  }
  return await response.json();
};

export const getQuizDetails = async (quizId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/${quizId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch details for quiz ID ${quizId}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching quiz details for ${quizId}:`, error);
    throw error;
  }
};

export const getArticleTitlePreview = async (url) => {
  try {
    if (url.includes("wikipedia.org/wiki/")) {
      const articleName = url.split("wiki/")[1].replace(/_/g, " ");
      return new Promise((resolve) =>
        setTimeout(
          () =>
            resolve(
              articleName.length > 0
                ? decodeURIComponent(articleName)
                : "Unknown Article"
            ),
          500
        )
      ); 
    }
    return null; 
  } catch (error) {
    console.error("Error fetching article title preview:", error);
    return null;
  }
};
