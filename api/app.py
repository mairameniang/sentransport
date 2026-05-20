import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Charger les données depuis les fichiers JSON
with open("lignes_ddd.json", "r") as f:
    lignes = json.load(f)

with open("arrets.json", "r") as f:
    arrets = json.load(f)


# Route d'accueil
@app.route("/")
def accueil():
    return jsonify({
        "message": "Bienvenue sur l'API SenTransport !",
        "endpoints": [
            "/lignes",
            "/lignes/<id>",
            "/arrets",
            "/stats",
            "/lignes/recherche?q=..."
        ]
    })


# Route : toutes les lignes
@app.route("/lignes")
def get_lignes():
    return jsonify(lignes)


# Route : une ligne par ID
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


# Route : tous les arrêts
@app.route("/arrets", methods=["GET"])
def get_arrets():
    return jsonify(arrets)


# Route : statistiques
@app.route("/stats", methods=["GET"])
def get_stats():

    nb_lignes = len(lignes)

    nb_total_arrets = sum(
        len(l["listeArrets"]) for l in lignes
    )

    ligne_plus_arrets = max(
        lignes,
        key=lambda l: len(l["listeArrets"])
    )["numero"]

    stats = {
        "nombre_lignes": nb_lignes,
        "nombre_total_arrets": nb_total_arrets,
        "ligne_plus_arrets": ligne_plus_arrets
    }

    return jsonify(stats)


# Route : recherche
@app.route("/lignes/recherche", methods=["GET"])
def recherche_lignes():

    # Récupérer le paramètre q
    q = request.args.get("q", "").lower()

    # Liste des résultats
    resultats = []

    # Parcourir les lignes
    for ligne in lignes:

        depart = ligne["depart"].lower()
        arrivee = ligne["arrivee"].lower()

        # Vérifier si q est dans départ ou arrivée
        if q in depart or q in arrivee:
            resultats.append(ligne)

    return jsonify(resultats)


# Lancer Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)