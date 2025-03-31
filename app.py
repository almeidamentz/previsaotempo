from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "95df597cfebe4c47b4d11232252903"  # 🔒 Insira sua chave correta aqui
CIDADES = ["Várzea Grande", "Cuiabá", "Goiás", "São Paulo", "Paraná", "Rio de Janeiro"]
URL_BASE = "https://api.weatherapi.com/v1/forecast.json"

# Página principal com a seleção da cidade
@app.route("/")
def index():
    return render_template("index.html", cidades=CIDADES)

# Rota para obter previsão do tempo da API
@app.route("/previsao")
def obter_previsao():
    cidade = request.args.get("cidade")
    
    if not cidade:
        return jsonify({"erro": "Cidade não informada"}), 400
    
    params = {
        "key": API_KEY,
        "q": cidade + ", BR",
        "days": 7,
        "lang": "pt"
    }

    try:
        resposta = requests.get(URL_BASE, params=params)
        resposta.raise_for_status()  
        dados = resposta.json()
        
        previsao = []
        for dia in dados["forecast"]["forecastday"]:
            previsao.append({
                "data": dia["date"],
                "temp_min": dia["day"]["mintemp_c"],
                "temp_max": dia["day"]["maxtemp_c"],
                "descricao": dia["day"]["condition"]["text"],
                "icon": "https:" + dia["day"]["condition"]["icon"]
            })
        
        return jsonify(previsao)

    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Falha na API: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
