// mainepadfinder-app/frontend/src/pages/Properties.jsx
import { useEffect, useState } from "react";

export default function Properties() {
  const [listings, setListings] = useState([]);
  const [city, setCity] = useState("");
  const [minRent, setMinRent] = useState("");
  const [maxRent, setMaxRent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // This is the important "const response / const data" pattern
  const loadListings = async (e) => {
    if (e) e.preventDefault(); // so it works as a form submit handler
    setLoading(true);
    setError("");

    try {
      const response = await fetch("https://localhost:5000/get_listings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          city: city || null,
          minRent: minRent ? Number(minRent) : null,
          maxRent: maxRent ? Number(maxRent) : null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || `Request failed with status ${response.status}`);
        setListings([]);
        return;
      }

      // THIS is where properties actually get stored
      setListings(data);
    } catch (err) {
      console.error("Error loading listings:", err);
      setError("Could not load listings (network error).");
      setListings([]);
    } finally {
      setLoading(false);
    }
  };

  // Fetch once on page load
  useEffect(() => {
    loadListings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div style={{ padding: "2rem 3rem" }}>
      <h2>Listings</h2>

      <form
        onSubmit={loadListings}
        style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem" }}
      >
        <input
          type="text"
          placeholder="City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <input
          type="number"
          placeholder="Min rent"
          value={minRent}
          onChange={(e) => setMinRent(e.target.value)}
        />
        <input
          type="number"
          placeholder="Max rent"
          value={maxRent}
          onChange={(e) => setMaxRent(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Search"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <p>
        <strong>{listings.length}</strong> listings found
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: "1rem",
        }}
      >
        {listings.map((l) => (
          <div
            key={l.PROPERTY_ID ?? l.id}
            style={{ border: "1px solid #ccc", padding: "1rem" }}
          >
            <h3>{l.UNIT_LABEL || l.title || "Untitled unit"}</h3>
            <p>
              {(l.CITY || l.city) || "Unknown city"},{" "}
              {(l.STATE_CODE || l.state) || "??"}
            </p>
            <p>
              <strong>${l.RENT_COST ?? l.rent}</strong> / month
            </p>
            <p>
              {(l.BEDROOMS ?? l.beds ?? "?")} bed •{" "}
              {(l.BATHROOMS ?? l.baths ?? "?")} bath
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}



