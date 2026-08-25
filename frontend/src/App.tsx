import './App.css'
import Login from "./pages/Login";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Register from "./pages/Register";
import HomePage from "./pages/HomePage";
import PaperDetailsPage from "./pages/PaperDetailsPage";
import SavedPapersPage from "./pages/SavedPapersPage";
import ProtectedRoute from "./components/ProtectedRoute";
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
            <Route
              path="/login"
              element={<Login />}
            />
            <Route
              path="/register"
              element={<Register />}
            />
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
                element={
                    <ProtectedRoute>
                        <MyAnalysesPage />
                    </ProtectedRoute>
                }
            />
          </Routes>
        </BrowserRouter>
      </WorkspaceProvider>
    </SavedPapersProvider>
  );
  
}
export default App;
