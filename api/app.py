import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Charger les données depuis le fichier JSON
with open("lignes_ddd.json", "r") as f:
    lignes = json.load(f)

@app.route("/")
def accueil():
    return jsonify({
        "message": "Bienvenue sur l'API SenTransport !",
        "endpoints": ["/lignes", "/lignes/<id>"]
    })

@app.route("/lignes")
def get_lignes():
    return jsonify(lignes)

@app.route("/lignes/<int:ligne_id>")
def get_ligne(ligne_id):

    ligne = next(
        (l for l in lignes if l["id"] == ligne_id),
        None
    )

    if ligne is None:
        return jsonify({
            "erreur": "Ligne non trouvée"
        }), 404

    return jsonify(ligne)

@app.route("/arrets", methods=["GET"])
def get_arrets():
    tous_arrets = []
    for ligne in lignes:
        tous_arrets.extend(ligne["listeArrets"])
    arrets_uniques = list(set(tous_arrets))
    return jsonify(arrets_uniques)

@app.route("/stats", methods=["GET"])
def get_stats():
    nb_lignes = len(lignes)
    nb_total_arrets = sum(len(l["listeArrets"]) for l in lignes)
    ligne_plus_arrets = max(lignes, key=lambda l: len(l["listeArrets"]))["numero"]

    stats = {
        "nombre_lignes": nb_lignes,
        "nombre_total_arrets": nb_total_arrets,
        "ligne_plus_arrets": ligne_plus_arrets
    }
    return jsonify(stats)

from flask import request  # ajoute cette ligne en haut si elle n’y est pas déjà

@app.route("/lignes/recherche", methods=["GET"])
def recherche_lignes():
    # 1️⃣ Récupérer le paramètre q
    q = request.args.get("q", "").lower()

    # 2️⃣ Créer une liste pour stocker les résultats
    resultats = []

    # 3️⃣ Parcourir toutes les lignes
    for ligne in lignes:
        depart = ligne["depart"].lower()
        arrivee = ligne["arrivee"].lower()

        # 4️⃣ Vérifier si q est dans le départ ou l’arrivée
        if q in depart or q in arrivee:
            resultats.append(ligne)

    # 5️⃣ Retourner les résultats
    return jsonify(resultats)



if __name__ == "__main__":
    app.run(debug=True, port=5000)

