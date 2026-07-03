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
  const path =
    "E:/YTDown_YouTube_Learn-OWASP-ZAP-In-8-Minutes-Automated-H_Media_WGSGGgMd9Fo_002_720p.mp4";

  const videoSrc = `http://127.0.0.1:8000/media?path=${encodeURIComponent(path)}`;

  return (
    <div style={{ padding: 32, fontFamily: "system-ui" }}>
      <h1>React + Python Desktop</h1>
      <p>
        Backend says: <strong>{msg}</strong>
      </p>
      <button
        onClick={async () => {
          const response = await window.pywebview.api.open_file_dialog();
          console.log(response);
        }}
      >
        Open file
      </button>
      <video controls width={600}>
        <source src={videoSrc} type="video/mp4" />
      </video>
    </div>
  );
}
