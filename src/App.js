import { useState } from 'react';
import './App.css';
import Header from './Header';
import Recherche from './Recherche';
import LigneBus from './LigneBus';
import DetailLigne from './DetailLigne';
import Footer from './Footer';

function App() {

  const [recherche, setRecherche] = useState("");
  const [ligneSelectionnee, setLigneSelectionnee] = useState(null);

  // ✅ Données complètes
  const lignes = [
    {
      id: 1,
      numero: "7",
      depart: "Pikine",
      arrivee: "Plateau",
      arrets: 12,
      listeArrets: ["Pikine", "Grand Yoff", "Liberté", "Plateau"]
    },
    {
      id: 2,
      numero: "15",
      depart: "Guédiawaye",
      arrivee: "Almadies",
      arrets: 10,
      listeArrets: ["Guédiawaye", "Foire", "Ouakam", "Almadies"]
    },
    {
      id: 3,
      numero: "9",
      depart: "Parcelles",
      arrivee: "Dakar Centre",
      arrets: 8,
      listeArrets: ["Parcelles", "Sacre Coeur", "Grand Dakar", "Centre"]
    }
  ];

  // 🔍 Filtrage
  const lignesFiltrees = lignes.filter(l =>
    l.depart.toLowerCase().includes(recherche.toLowerCase()) ||
    l.arrivee.toLowerCase().includes(recherche.toLowerCase()) ||
    l.numero.includes(recherche)
  );

  // 👆 clic sur une ligne
  function handleClickLigne(ligne) {
    if (ligneSelectionnee && ligneSelectionnee.id === ligne.id) {
      setLigneSelectionnee(null);
    } else {
      setLigneSelectionnee(ligne);
    }
  }

  return (
    <div className="App">

      <Header />

      <main className="contenu">

        <Recherche
          valeur={recherche}
          onChange={setRecherche}
        />

        <p className="resultat-recherche">
          {lignesFiltrees.length} ligne
          {lignesFiltrees.length > 1 ? 's' : ''} trouvée
          {lignesFiltrees.length > 1 ? 's' : ''}
        </p>

        {lignesFiltrees.map(ligne => (
          <LigneBus
            key={ligne.id}
            numero={ligne.numero}
            depart={ligne.depart}
            arrivee={ligne.arrivee}
            arrets={ligne.arrets}
            estSelectionnee={
              ligneSelectionnee &&
              ligneSelectionnee.id === ligne.id
            }
            onClick={() => handleClickLigne(ligne)}
          />
        ))}

        {ligneSelectionnee && (
          <DetailLigne ligne={ligneSelectionnee} />
        )}

      </main>

      <Footer />

    </div>
  );
}

export default App;