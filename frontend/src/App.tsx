import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import PaperDetailsPage from "./pages/PaperDetailsPage";
import SavedPapersPage from "./pages/SavedPapersPage";
import MyAnalysesPage from "./pages/MyAnalysesPage";
import AIWorkspacePage from "./pages/AIWorkspacePage";
import { SavedPapersProvider } from "./context/SavedPapersContext";
import { WorkspaceProvider } from "./context/WorkspaceContext";

function App() {
  return (
    <SavedPapersProvider>
      <WorkspaceProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<Layout />}>
                <Route
                    path="/"
                    element={<HomePage />}
                />
                <Route
                    path="/paper/:arxiv_id"
                    element={<PaperDetailsPage />}
                />
            </Route>
            <Route
              path="/saved"
              element={<SavedPapersPage />}
            />
            <Route
                path="/workspace"
                element={<AIWorkspacePage />}
            />
            <Route
                path="/analyses"
                element={<MyAnalysesPage />}
            />
          </Routes>
        </BrowserRouter>
      </WorkspaceProvider>
    </SavedPapersProvider>
  );
  
}
export default App;
