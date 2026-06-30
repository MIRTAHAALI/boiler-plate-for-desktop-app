import { useEffect, useState } from "react";

export default function App() {
  const [msg, setMsg] = useState("Loading...");

  useEffect(() => {
  const timer = setInterval(async () => {
    if (window.pywebview?.api) {
      clearInterval(timer);

      const response = await window.pywebview.api.say_hello("Taha");
      setMsg(response);
    }
  }, 100);

  return () => clearInterval(timer);
}, []);

  return (
    <div style={{ padding: 32, fontFamily: "system-ui" }}>
      <h1>React + Python Desktop</h1>
      <p>
        Backend says: <strong>{msg}</strong>
      </p>
    </div>
  );
}
