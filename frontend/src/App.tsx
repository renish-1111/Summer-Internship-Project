import { BrowserRouter, Routes, Route } from "react-router-dom";
import Demo from "./demo";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Demo />} />
      </Routes>
    </BrowserRouter>
  );
}

