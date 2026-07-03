import "./LoadingSpinner.css";

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>

      <h2>Searching papers...</h2>

      <p>Please wait while we fetch the latest research papers.</p>
    </div>
  );
}

export default LoadingSpinner;