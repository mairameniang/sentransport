function LigneBus({ numero, depart, arrivee, onClick, estSelectionnee }) {
  return (
    <div
      onClick={onClick}
      style={{
        padding: "10px",
        margin: "10px",
        border: "1px solid black",
        cursor: "pointer",
        background: estSelectionnee ? "#d1f0ff" : "white"
      }}
    >
      <h3>Ligne {numero}</h3>
      <p>{depart} → {arrivee}</p>
    </div>
  );
}

export default LigneBus;