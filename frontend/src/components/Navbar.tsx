import { NavLink } from "react-router-dom";
import { House, Bookmark, Sparkles,FileText,LogIn,LogOut, } from "lucide-react";
import { useAuth } from "../auth/Authcontext";
import "./Navbar.css"

type NavbarProps = {

  title: string;

  subtitle: string;

};

function Navbar({ title, subtitle }: NavbarProps) {

    const { isAuthenticated, logout } = useAuth();

  return (
    <header className="navbar">
      <div className="navbar-brand">
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
      <nav className="navbar-links">
          <NavLink
              to="/"
              className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
              }
          >
              <House size={22} />
              <span>Home</span>
          </NavLink>

          <NavLink
              to="/saved"
              className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
              }
          >
              <Bookmark size={22} />
              <span>Saved Papers</span>
          </NavLink>

          <NavLink
              to="/workspace"
              className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
              }
          >
              <Sparkles size={22} />
              <span>AI Workspace</span>
          </NavLink>

          <NavLink
              to="/analyses"
              className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
              }
          >
              <FileText size={22} />
              <span>My Analyses</span>
          </NavLink>
          {isAuthenticated ? (
                <button
                    className="nav-link auth-button"
                    onClick={logout}
                >
                    <LogOut size={22} />
                    <span>Logout</span>
                </button>
            ) : (
                <NavLink
                    to="/login"
                    className={({ isActive }) =>
                        isActive ? "nav-link active" : "nav-link"
                    }
                >
                    <LogIn size={22} />
                    <span>Login</span>
                </NavLink>
            )}
      </nav>
    </header>
  );
}

export default Navbar;