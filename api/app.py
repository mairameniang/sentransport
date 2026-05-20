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


# =========================
# INCIDENTS
# =========================
incidents = []

@app.route("/incidents", methods=["GET"])
def get_incidents():
    return jsonify(incidents)


@app.route("/incidents", methods=["POST"])
def post_incident():
    data = request.get_json()

    if not data or "ligne" not in data or "description" not in data:
        return jsonify(
            {"erreur": "Champs requis manquants"}
        ), 400

    incident = {
        "id": len(incidents) + 1,
        "ligne": data["ligne"],
        "description": data["description"],
        "lieu": data.get("lieu", "Non precise"),
    }

    incidents.append(incident)

    return jsonify(incident), 201


# =========================
# ROUTES API
# =========================

@app.route("/")
def accueil():
    return jsonify({
        "message": "Bienvenue sur l'API SenTransport !",
        "endpoints": [
            "/lignes",
            "/lignes/<id>",
            "/arrets",
            "/stats",
            "/lignes/recherche?q=...",
            "/incidents"
        ]
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
        return jsonify({"erreur": "Ligne non trouvée"}), 404

    return jsonify(ligne)


@app.route("/arrets", methods=["GET"])
def get_arrets():
    return jsonify(arrets)


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

    return jsonify({
        "nombre_lignes": nb_lignes,
        "nombre_total_arrets": nb_total_arrets,
        "ligne_plus_arrets": ligne_plus_arrets
    })


@app.route("/lignes/recherche", methods=["GET"])
def recherche_lignes():
    q = request.args.get("q", "").lower()

    resultats = []

    for ligne in lignes:
        depart = ligne["depart"].lower()
        arrivee = ligne["arrivee"].lower()

        if q in depart or q in arrivee:
            resultats.append(ligne)

    return jsonify(resultats)


# =========================
# LANCEMENT
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)