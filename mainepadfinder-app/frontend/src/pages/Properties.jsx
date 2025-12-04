// mainepadfinder-app/frontend/src/pages/Properties.jsx
import { useState } from "react";

const PAGE_SIZE = 10;

export default function Properties() {
  const [city, setCity] = useState("");
  const [minRent, setMinRent] = useState("");
  const [maxRent, setMaxRent] = useState("");
  const [minBeds, setMinBeds] = useState("");
  const [minBaths, setMinBaths] = useState("");
  const [properties, setProperties] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Helper: call backend with either filters or no filters
  async function fetchProperties({ useFilters }) {
    setLoading(true);
    setError("");

    const body = {};

    //filters on properties page 
    if (useFilters) {
      body.city = city.trim() || null;
      body.minRent = minRent === "" ? null : Number(minRent);
      body.maxRent = maxRent === "" ? null : Number(maxRent);
      body.minBeds = minBeds === "" ? null : Number(minBeds);
      body.minBaths = minBaths === "" ? null : Number(minBaths);
    } else {
      // Explicitly send no filters
      body.city = null;
      body.minRent = null;
      body.maxRent = null;
      body.minBeds = null;
      body.minBaths = null;
    }

    try {
      const response = await fetch("https://localhost:5000/api/properties", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", 
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || `Request failed with status ${response.status}`);
        setProperties([]);
        setPage(1);
        return;
      }

      setProperties(data);
      setPage(1); // reset to first page on new search
    } catch (err) {
      console.error("Error loading properties:", err);
      setError("Could not load properties (network error).");
      setProperties([]);
      setPage(1);
    } finally {
      setLoading(false);
    }
  }

  const handleApplyFilters = (e) => {
    e.preventDefault();
    fetchProperties({ useFilters: true });
  };

  const handleNoFilters = (e) => {
    e.preventDefault();
    
    setCity("");
    setMinRent("");
    setMaxRent("");
    setMinBeds("");
    setMinBaths("");
    fetchProperties({ useFilters: false });
  };

  const totalResults = properties.length;
  const totalPages =
    totalResults === 0 ? 1 : Math.ceil(totalResults / PAGE_SIZE);
  const startIndex = (page - 1) * PAGE_SIZE;
  const currentSlice = properties.slice(startIndex, startIndex + PAGE_SIZE);

  const handlePrevPage = () => {
    if (page > 1) setPage((p) => p - 1);
  };

  const handleNextPage = () => {
    if (page < totalPages) setPage((p) => p + 1);
  };

  return (
    <div style={{ padding: "2rem 3rem" }}>
      <h2>Browse Properties</h2>
      <p style={{ maxWidth: "600px" }}>
        Apply filter below to find the perfect rental property in Maine!
      </p>

      {/* Filter Form */}
      <form
        onSubmit={handleApplyFilters}
        style={{
          margin: "1rem 0",
          display: "flex",
          flexWrap: "wrap",
          gap: "0.75rem",
          alignItems: "flex-end",
        }}
      >
        <div style={{ display: "flex", flexDirection: "column" }}>
          <label htmlFor="city">City</label>
          <input
            id="city"
            type="text"
            placeholder="e.g., Portland"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <label htmlFor="minRent">Min rent</label>
          <input
            id="minRent"
            type="number"
            placeholder="e.g., 800"
            value={minRent}
            onChange={(e) => setMinRent(e.target.value)}
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <label htmlFor="maxRent">Max rent</label>
          <input
            id="maxRent"
            type="number"
            placeholder="e.g., 1500"
            value={maxRent}
            onChange={(e) => setMaxRent(e.target.value)}
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <label htmlFor="minBeds">Min beds</label>
          <input
            id="minBeds"
            type="number"
            placeholder="e.g., 2"
            value={minBeds}
            onChange={(e) => setMinBeds(e.target.value)}
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <label htmlFor="minBaths">Min baths</label>
          <input
            id="minBaths"
            type="number"
            placeholder="e.g., 1"
            value={minBaths}
            onChange={(e) => setMinBaths(e.target.value)}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Apply filters"}
        </button>

        <button
          type="button"
          onClick={handleNoFilters}
          disabled={loading}
          style={{ marginLeft: "0.5rem" }}
        >
          {loading ? "Loading..." : "No filters"}
        </button>
      </form>

      {/* Error message */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Summary + pagination controls */}
      <div
        style={{
          marginBottom: "0.75rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "0.5rem",
        }}
      >
        <p>
          {totalResults === 0 ? (
            "No properties loaded yet."
          ) : (
            <>
              Showing{" "}
              <strong>
                {startIndex + 1}–{Math.min(startIndex + PAGE_SIZE, totalResults)}
              </strong>{" "}
              of <strong>{totalResults}</strong> properties (page{" "}
              <strong>{page}</strong> of <strong>{totalPages}</strong>)
            </>
          )}
        </p>

        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button onClick={handlePrevPage} disabled={page === 1 || totalResults === 0}>
            Previous
          </button>
          <button
            onClick={handleNextPage}
            disabled={page >= totalPages || totalResults === 0}
          >
            Next
          </button>
        </div>
      </div>

      {/* Results grid – VIEW ONLY */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: "1rem",
        }}
      >
        {currentSlice.map((p) => (
          <div
            key={p.id ?? p.PROPERTY_ID}
            style={{
              border: "1px solid #ccc",
              padding: "1rem",
              borderRadius: "8px",
              background: "#fafafa",
            }}
          >
            <h3>{p.title || p.UNIT_LABEL || "Untitled unit"}</h3>
            <p>
              {(p.city || p.CITY || "Unknown city")},{" "}
              {(p.state || p.STATE_CODE || "??")}
            </p>
            <p>
              <strong>${p.rent ?? p.RENT_COST}</strong> / month
            </p>
            <p>
              {(p.beds ?? p.BEDROOMS ?? "?")} bed •{" "}
              {(p.baths ?? p.BATHROOMS ?? "?")} bath
            </p>
            {(p.sqft ?? p.SQFT) && <p>{p.sqft ?? p.SQFT} sq ft</p>}
            {p.canRent ?? p.CAN_RENT ? (
              <p style={{ color: "green", fontWeight: "bold" }}>Available</p>
            ) : (
              <p style={{ color: "gray" }}>Not available</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

