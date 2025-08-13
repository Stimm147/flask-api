from flask import Flask, jsonify
from flask_cors import CORS

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# --- KLUCZOWA KONFIGURACJA CORS ---
# Zezwól na zapytania tylko z adresu URL Twojego frontendu.
# To jest dokładnie ten sam mechanizm, który konfigurowałeś w Reflex.
CORS(
    app,
    resources={
        r"/api/*": {"origins": "https://portfolio-production-3beb.up.railway.app"}
    },
)

# Proste dane w pamięci, które będzie zwracać nasze API
stats_data = {"page_visitors": 123, "projects_completed": 5, "api_status": "OK"}


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Zwraca dane statystyczne w formacie JSON."""
    return jsonify(stats_data)


# Ta część poniżej jest tylko do testów lokalnych, nie będzie używana na Railway
if __name__ == "__main__":
    app.run(debug=True, port=5001)
