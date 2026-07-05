import { NavLink } from "react-router-dom";

type NavbarProps = {

  title: string;

  subtitle: string;

};

function Navbar({ title, subtitle }: NavbarProps) {
  return (
    <header className="navbar">
      <div className="navbar-brand">
          <h2>{title}</h2>
          <p>{subtitle}</p>
      </div>
      <nav className="navbar-links">
          <NavLink to="/">🏠 Home</NavLink>
          <NavLink to="/saved">
              ❤️ Saved Papers
          </NavLink>
          <NavLink to="/workspace">
              🤖 AI Workspace
          </NavLink>
      </nav>
    </header>
  );
}

export default Navbar;