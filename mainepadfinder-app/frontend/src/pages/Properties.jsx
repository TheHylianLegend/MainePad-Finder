import { useState } from "react";

export default function Properties() {
  const [city, setCity] = useState("");
  const [minRent, setMinRent] = useState("");
  const [maxRent, setMaxRent] = useState("");
  const [properties, setProperties] = useState([]);
  const [error, setError] = useState("");

  const handleSearch = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("https://localhost:5000/api/properties", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // same as login/signup
        body: JSON.stringify({
          city,
          minRent: minRent === "" ? null : Number(minRent),
          maxRent: maxRent === "" ? null : Number(maxRent),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || `Request failed with status ${response.status}`);
        setProperties([]);
      } else {
        setProperties(data);
      }
    } catch (err) {
      console.error("Error loading properties:", err);
      setError("Network error");
      setProperties([]);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Properties</h1>

      <form onSubmit={handleSearch} style={{ marginBottom: "1rem" }}>
        <div>
          <label>City:&nbsp;</label>
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </div>

        <div>
          <label>Min rent:&nbsp;</label>
          <input
            type="number"
            value={minRent}
            onChange={(e) => setMinRent(e.target.value)}
          />
        </div>

        <div>
          <label>Max rent:&nbsp;</label>
          <input
            type="number"
            value={maxRent}
            onChange={(e) => setMaxRent(e.target.value)}
          />
        </div>

        <button type="submit" style={{ marginTop: "0.5rem" }}>
          Search
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {properties.map((p) => (
          <li key={p.id ?? p.PROPERTY_ID}>
            {(p.title || p.UNIT_LABEL || "Untitled")} — $
            {p.rent ?? p.RENT_COST} —{" "}
            {(p.city || p.CITY || "Unknown city")},{" "}
            {(p.state || p.STATE_CODE || "??")}
          </li>
        ))}
      </ul>
    </div>
  );
}
