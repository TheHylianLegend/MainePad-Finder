import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/hello")
      .then(response => response.json())
      .then(data => setData(data.message));
  }, []);

  return (
    <>
      <h1>React + Flask Test</h1>
      <p>{data}</p>
    </>
  );
}

export default App;
