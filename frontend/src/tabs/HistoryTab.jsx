// frontend/src/tabs/HistoryTab.jsx
import React, { useState, useEffect } from "react";
import { getQuizHistory, getQuizDetails } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner";
import Modal from "../components/QuizModal";
import QuizDisplay from "../components/QuizDisplay";
import HistoryTable from "../components/HistoryTable";

function HistoryTab() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedQuizDetails, setSelectedQuizDetails] = useState(null);
  const [modalLoading, setModalLoading] = useState(false);

  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getQuizHistory();
        const sortedData = data.sort(
          (a, b) => new Date(b.date_generated) - new Date(a.date_generated)
        );
        setHistory(sortedData);
      } catch (err) {
        setError(err.message || "Failed to fetch quiz history.");
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const handleDetailsClick = async (quizId) => {
    setError(null);
    setSelectedQuizDetails(null); // Clear previous details
    setIsModalOpen(true); // Open modal
    setModalLoading(true); // Start modal loading

    try {
      const details = await getQuizDetails(quizId);
      setSelectedQuizDetails(details);
    } catch (err) {
      setError(err.message || "Failed to load quiz details.");
    } finally {
      setModalLoading(false); // Stop modal loading
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedQuizDetails(null);
    setError(null);
    setModalLoading(false);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  // Only show error if initial history fetch failed completely and there's no data
  if (error && !history.length && !isModalOpen) {
    return (
      <div className="p-4 text-center text-red-500 dark:text-red-400">
        <p>{error}</p>
        <p className="mt-2">
          Please ensure the server is running and accessible at
          `https://ai-quiz-backend-2nwj.onrender.com`.
        </p>
      </div>
    );
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-6 text-gray-800 dark:text-gray-200">
        Past Quizzes (History)
      </h2>

      {/* HistoryTable component here */}
      <HistoryTable history={history} handleDetailsClick={handleDetailsClick} />

      {/* Quiz Details Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title={
          selectedQuizDetails?.title
            ? `${selectedQuizDetails.title} Quiz Details`
            : "Quiz Details"
        }
      >
        {error && (
          <p className="text-red-500 dark:text-red-400 mb-4">{error}</p>
        )}
        {modalLoading ? ( //  modalLoading state
          <LoadingSpinner isGenerateTab={false} />
        ) : selectedQuizDetails ? (
          <QuizDisplay quizData={selectedQuizDetails} />
        ) : (
          !error && (
            <p className="text-center text-gray-500 dark:text-gray-400">
              Loading quiz details...
            </p>
          )
        )}
      </Modal>
    </div>
  );
}

export default HistoryTab;
