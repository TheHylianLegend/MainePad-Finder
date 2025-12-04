// mainepadfinder-app/frontend/src/pages/Listings.jsx
import { useState } from "react";

export default function Listings() {
  const [listings, setListings] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadListings() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch("https://localhost:5000/api/properties", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        // Load all properties: no filters
        body: JSON.stringify({
          city: null,
          minRent: null,
          maxRent: null,
          minBeds: null,
          minBaths: null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || `Request failed with status ${response.status}`);
        setListings([]);
        setSelected(null);
        return;
      }

      setListings(data);
      setSelected(data.length > 0 ? data[0] : null); // auto-select first
    } catch (err) {
      console.error("Error loading listings:", err);
      setError("Could not load listings (network error).");
      setListings([]);
      setSelected(null);
    } finally {
      setLoading(false);
    }
  }

  function handleSelect(listing) {
    setSelected(listing);
  }

  // Helper to handle mixed key names 
  function normalize(listing) {
    if (!listing) return null;
    return {
      id: listing.id ?? listing.PROPERTY_ID,
      title: listing.title ?? listing.UNIT_LABEL ?? "Untitled unit",
      city: listing.city ?? listing.CITY ?? "Unknown city",
      state: listing.state ?? listing.STATE_CODE ?? "??",
      rent: listing.rent ?? listing.RENT_COST,
      beds: listing.beds ?? listing.BEDROOMS,
      baths: listing.baths ?? listing.BATHROOMS,
      sqft: listing.sqft ?? listing.SQFT,
      canRent:
        typeof listing.canRent === "boolean"
          ? listing.canRent
          : Boolean(listing.CAN_RENT),
      raw: listing,
    };
  }

  const normalizedSelected = normalize(selected);

  return (
    <div style={{ padding: "2rem 3rem" }}>
      <h2>Listings</h2>
      <p style={{ maxWidth: "650px" }}>
        Load listings from the database and view details for each rental 
      </p>

      {/* Top controls */}
      <div
        style={{
          margin: "1rem 0",
          display: "flex",
          alignItems: "center",
          gap: "1rem",
          flexWrap: "wrap",
        }}
      >
        <button onClick={loadListings} disabled={loading}>
          {loading ? "Loading..." : "Load listings"}
        </button>

        <span>
          {listings.length > 0 ? (
            <strong>{listings.length}</strong>
          ) : (
            "No listings loaded yet"
          )}{" "}
        </span>

        {error && <span style={{ color: "red" }}>{error}</span>}
      </div>

      {/* Main layout: list on the left, details on the right */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(220px, 1.2fr) 2fr",
          gap: "1.5rem",
          minHeight: "300px",
        }}
      >
        {/* Left: list of listings */}
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "0.5rem",
            maxHeight: "480px",
            overflowY: "auto",
            background: "#fafafa",
          }}
        >
          {listings.length === 0 && (
            <p style={{ padding: "0.5rem" }}>
              Click Load Listings to display available properties
            </p>
          )}

          {listings.map((l) => {
            const n = normalize(l);
            const isActive = selected && n.id === normalizedSelected?.id;

            return (
              <button
                key={n.id}
                type="button"
                onClick={() => handleSelect(l)}
                style={{
                  width: "100%",
                  textAlign: "left",
                  border: "none",
                  borderRadius: "6px",
                  padding: "0.5rem 0.75rem",
                  marginBottom: "0.35rem",
                  cursor: "pointer",
                  background: isActive ? "#e0f2ff" : "white",
                  boxShadow: isActive
                    ? "0 0 0 1px #3b82f6"
                    : "0 0 0 1px #e5e7eb",
                }}
              >
                <div style={{ fontWeight: 600 }}>{n.title}</div>
                <div style={{ fontSize: "0.9rem", color: "#555" }}>
                  {n.city}, {n.state}
                </div>
                <div style={{ fontSize: "0.9rem", marginTop: "0.15rem" }}>
                  {n.beds ?? "?"} bed • {n.baths ?? "?"} bath
                </div>
                <div style={{ fontSize: "0.9rem", marginTop: "0.15rem" }}>
                  <strong>${n.rent}</strong> / month
                </div>
              </button>
            );
          })}
        </div>

        {/* Right: detail view */}
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "1rem 1.25rem",
            minHeight: "250px",
          }}
        >
          {!normalizedSelected ? (
            <p>Select a listing on the left to see details.</p>
          ) : (
            <>
              <h3 style={{ marginTop: 0 }}>{normalizedSelected.title}</h3>
              <p style={{ margin: "0.25rem 0 0.5rem 0", color: "#555" }}>
                {normalizedSelected.city}, {normalizedSelected.state}
              </p>

              <p style={{ fontSize: "1.1rem" }}>
                <strong>${normalizedSelected.rent}</strong> / month
              </p>

              <p>
                <strong>Bedrooms:</strong> {normalizedSelected.beds ?? "Unknown"}
              </p>
              <p>
                <strong>Bathrooms:</strong>{" "}
                {normalizedSelected.baths ?? "Unknown"}
              </p>
              {normalizedSelected.sqft && (
                <p>
                  <strong>Square footage:</strong> {normalizedSelected.sqft} sq ft
                </p>
              )}

              <p>
                <strong>Status:</strong>{" "}
                {normalizedSelected.canRent ? (
                  <span style={{ color: "green", fontWeight: "bold" }}>
                    Available to rent
                  </span>
                ) : (
                  <span style={{ color: "gray" }}>Not currently available</span>
                )}
              </p>

              <p>
                <strong>Internal ID:</strong> {normalizedSelected.id}
              </p>

              <hr style={{ margin: "1rem 0" }} />

              <p style={{ fontSize: "0.9rem", color: "#666" }}>
                I will put more info here like contact landlord or a way to favorite the listing 
                (save for later)
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
