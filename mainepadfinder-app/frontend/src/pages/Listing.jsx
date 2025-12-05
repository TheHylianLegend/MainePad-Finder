// mainepadfinder-app/frontend/src/pages/Listing.jsx
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useMemo } from "react";

export default function Listing() {
  const location = useLocation();
  const navigate = useNavigate();
  const { id } = useParams(); // /listing/:id

  const property = location.state?.property || null;
  const allProperties = location.state?.allProperties || null;

  // Interpret availability CAN_RENT = available 
  function isAvailableFromRaw(p) {
    if (!p) return false;

    const raw = "canRent" in p ? p.canRent : p.CAN_RENT;

    if (typeof raw === "boolean") {
      // false (from 0) = available, true (from 1) = not
      return raw === false;
    }

    if (typeof raw === "number") {
      return raw === 0; // 0 = available
    }

    if (raw === null || raw === undefined) {
      // unknown treat as available
      return true;
    }

    return false;
  }

  function formatBedsDetail(beds) {
    if (beds === 0) return "Studio";
    if (beds == null) return "Unknown";
    if (beds === 1) return "1 bedroom";
    return `${beds} bedrooms`;
  }

  // Normalize everything we care about
  function normalize(p) {
    if (!p) return null;
    const available = isAvailableFromRaw(p);

    const city = p.city ?? p.CITY ?? "Unknown city";
    const state = p.state ?? p.STATE_CODE ?? "??";

    const addressLine1 = p.addressLine1 ?? p.ADDRESS_LINE1 ?? null;
    const addressLine2 = p.addressLine2 ?? p.ADDRESS_LINE2 ?? null;
    const zipCode = p.zipCode ?? p.ZIP_CODE ?? null;

    const unitLabel = p.unitLabel ?? p.UNIT_LABEL ?? null;

    // Our heading is address if we have it, otherwise city + state
    let heading = addressLine1;
    if (!heading) {
      heading = `${city}, ${state}`;
    }

    return {
      id: p.id ?? p.PROPERTY_ID ?? id,
      heading,
      addressLine1,
      addressLine2,
      city,
      state,
      zipCode,
      unitLabel,
      rent: p.rent ?? p.RENT_COST,
      beds: p.beds ?? p.BEDROOMS,
      baths: p.baths ?? p.BATHROOMS,
      sqft: p.sqft ?? p.SQFT,
      canRent: available,
      landlordName: p.landlordName ?? p.LANDLORD_NAME ?? null,
      landlordEmail: p.landlordEmail ?? p.LANDLORD_EMAIL ?? null,
      raw: p,
    };
  }

  const n = normalize(property);

  // Prev and Next navigation for listing page
  const { indexInList, totalInList } = useMemo(() => {
    if (!allProperties || !property) return { indexInList: null, totalInList: null };

    const thisId = property.id ?? property.PROPERTY_ID ?? id;
    const idx = allProperties.findIndex(
      (p) => (p.id ?? p.PROPERTY_ID) === thisId
    );

    return {
      indexInList: idx === -1 ? null : idx,
      totalInList: allProperties.length,
    };
  }, [allProperties, property, id]);

  function goToIndex(newIndex) {
    if (!allProperties || newIndex == null) return;
    if (newIndex < 0 || newIndex >= allProperties.length) return;

    const nextProp = allProperties[newIndex];
    const nextId = nextProp.id ?? nextProp.PROPERTY_ID;

    navigate(`/listing/${nextId}`, {
      state: { property: nextProp, allProperties },
    });
  }

  function handlePrev() {
    if (indexInList == null) return;
    goToIndex(indexInList - 1);
  }

  function handleNext() {
    if (indexInList == null) return;
    goToIndex(indexInList + 1);
  }

  // If user hit /listing/:id directly, show message 
  if (!property || !n) {
    return (
      <div style={{ padding: "2rem 3rem" }}>
        <button
          type="button"
          onClick={() => navigate("/properties")}
          style={{
            marginBottom: "1rem",
            padding: "0.4rem 0.9rem",
            borderRadius: "999px",
            border: "1px solid #e5e7eb",
            background: "white",
            cursor: "pointer",
          }}
        >
          ← Back to Properties
        </button>
        <h2>Listing not loaded</h2>
        <p style={{ maxWidth: "520px" }}>
          We couldn&apos;t load this listing directly. Please go back to the{" "}
          <strong>Properties</strong> page and click on a property to view its
          details.
        </p>
      </div>
    );
  }

  return (
    <div style={{ padding: "2rem 3rem" }}>
      <button
        type="button"
        onClick={() => navigate(-1)}
        style={{
          marginBottom: "1rem",
          padding: "0.4rem 0.9rem",
          borderRadius: "999px",
          border: "1px solid #e5e7eb",
          background: "white",
          cursor: "pointer",
        }}
      >
        ← Back to Properties
      </button>

      {indexInList != null && totalInList != null && (
        <p style={{ margin: "0 0 0.75rem 0", color: "#555" }}>
          Listing <strong>{indexInList + 1}</strong> of{" "}
          <strong>{totalInList}</strong>
        </p>
      )}

      <div
        style={{
          border: "1px solid #e5e7eb",
          borderRadius: "12px",
          padding: "1.5rem 1.75rem",
          maxWidth: "720px",
          background: "#ffffff",
          boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
        }}
      >
        {/* Big heading = address or city/state */}
        <h2 style={{ marginTop: 0 }}>{n.heading}</h2>

        {/* Full address block */}
        <div style={{ marginBottom: "0.75rem", color: "#555" }}>
          {n.addressLine1 && <div>{n.addressLine1}</div>}
          {n.addressLine2 && <div>{n.addressLine2}</div>}
          <div>
            {n.city}, {n.state} {n.zipCode || ""}
          </div>
        </div>

        {/* Unit number */}
        <p>
          <strong>Unit: </strong>
          {n.unitLabel || "N/A"}
        </p>

        {/* Rent */}
        <p style={{ fontSize: "1.2rem" }}>
          <strong>${n.rent}</strong> / month
        </p>

        {/* Beds & baths */}
        <p>
          <strong>Bedrooms: </strong>
          {formatBedsDetail(n.beds)}
        </p>
        <p>
          <strong>Bathrooms: </strong>
          {n.baths ?? "Unknown"}
        </p>

        {/* Optional sqft */}
        {n.sqft && (
          <p>
            <strong>Square footage: </strong>
            {n.sqft} sq ft
          </p>
        )}

        {/* Availability */}
        <p>
          <strong>Status: </strong>
          {n.canRent ? (
            <span style={{ color: "green", fontWeight: "bold" }}>
              Available to rent
            </span>
          ) : (
            <span style={{ color: "gray" }}>Not currently available</span>
          )}
        </p>

        {/* Landlord */}
        <p>
          <strong>Landlord: </strong>
          {n.landlordName ? n.landlordName : "Not specified"}
        </p>
        {n.landlordEmail && (
          <p>
            <strong>Contact email: </strong>
            <a href={`mailto:${n.landlordEmail}`}>{n.landlordEmail}</a>
          </p>
        )}

        <p>
          <strong>Internal ID: </strong>
          {n.id}
        </p>

        <hr style={{ margin: "1rem 0" }} />

        {indexInList != null && totalInList != null && totalInList > 1 && (
          <div
            style={{
              marginTop: "1rem",
              display: "flex",
              justifyContent: "space-between",
              gap: "0.5rem",
              flexWrap: "wrap",
            }}
          >
            <button
              type="button"
              onClick={handlePrev}
              disabled={indexInList <= 0}
              style={{
                padding: "0.4rem 0.9rem",
                borderRadius: "999px",
                border: "1px solid #e5e7eb",
                background:
                  indexInList <= 0 ? "#f9fafb" : "white",
                cursor: indexInList <= 0 ? "default" : "pointer",
              }}
            >
              ← Previous listing
            </button>
            <button
              type="button"
              onClick={handleNext}
              disabled={indexInList >= totalInList - 1}
              style={{
                padding: "0.4rem 0.9rem",
                borderRadius: "999px",
                border: "1px solid #e5e7eb",
                background:
                  indexInList >= totalInList - 1 ? "#f9fafb" : "white",
                cursor:
                  indexInList >= totalInList - 1 ? "default" : "pointer",
              }}
            >
              Next listing →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

