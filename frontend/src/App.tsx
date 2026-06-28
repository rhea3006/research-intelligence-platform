import { useState } from 'react'
import './App.css'
import Navbar from "./components/Navbar";

function App() {
  return (
    <>
      <Navbar
      title="Research Intelligence Platform"
      subtitle="Search smarter. Discover faster."
      />
      <main>
        <p>Welcome to my research paper search engine.</p>
      </main>
    </>
  );
}
export default App;
