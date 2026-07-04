import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import PaperDetailsPage from "./pages/PaperDetailsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route
          path="/paper/:arxiv_id"

          element={<PaperDetailsPage />}
        />
      </Routes>
    </BrowserRouter>
  );
  
}
export default App;
