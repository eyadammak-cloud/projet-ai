from flask import Flask, render_template
import json

app = Flask(__name__)

# ✅ Charger les produits depuis un fichier JSON
def charger_produits():
    with open("produits.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ✅ Page d'accueil : liste de produits
@app.route("/", methods=["GET"])
def index():
    produits = charger_produits()
    return render_template("index.html", produits=produits)

# ✅ Page produit avec bouton "essayer sur la main"
@app.route("/produit/<int:produit_id>", methods=["GET"])
def produit(produit_id):
    produits = charger_produits()
    produit = next((p for p in produits if p["id"] == produit_id), None)
    if not produit:
        return "Produit non trouvé", 404
    return render_template("produit.html", produit=produit)

# ✅ Initialisation du fichier produits.json (à exécuter 1 fois)
if __name__ == "__main__":
    produits = [
        {
            "id": 1,
            "nom": "Bague dorée",
            "image": "image1.jpg",
            "description": "Une magnifique bague en acier doré.",
            "prix": 29.99
        },
        {
            "id": 2,
            "nom": "Bague houta",
            "image": "image2.jpg",
            "description": "Une bague fine et élégante.",
            "prix": 19.99
        },
        {
            "id": 3,
            "nom": "Bague rainbow",
            "image": "image3.jpg",
            "description": "Une bague colorée",
            "prix": 7
        }
    ]
    with open("produits.json", "w", encoding="utf-8") as f:
        json.dump(produits, f, indent=4, ensure_ascii=False)
    
    app.run(debug=True)
