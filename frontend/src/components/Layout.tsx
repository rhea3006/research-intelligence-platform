import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

function Layout() {
  return (
    <>
      <Navbar
        title="Research Intelligence Platform"
        subtitle="Search smarter. Discover faster."
      />

      <main>
        <Outlet />
      </main>
    </>
  );
}

export default Layout;
