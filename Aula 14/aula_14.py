from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

URL_FRUITYVICE = "https://www.fruityvice.com/api/fruit/"


sucos = []
proximo_id = 1


class FrutaNaoEncontrada(Exception):
    pass


class ErroFruityvice(Exception):
    pass


@app.errorhandler(FrutaNaoEncontrada)
def tratar_fruta_nao_encontrada(erro):
    return jsonify({"erro": f"Fruta '{erro}' não encontrada. Tente o nome em inglês, ex: banana, strawberry."}), 404


@app.errorhandler(ErroFruityvice)
def tratar_erro_fruityvice(erro):
    return jsonify({"erro": "Não foi possível consultar a API Fruityvice. Tente novamente mais tarde."}), 503



def buscar_fruta(nome):
    
    try:
        resposta = requests.get(URL_FRUITYVICE + nome.strip().lower(), timeout=10)
    except requests.RequestException:
        raise ErroFruityvice()

    if resposta.status_code == 404:
        raise FrutaNaoEncontrada(nome)
    if resposta.status_code != 200:
        raise ErroFruityvice()

    dados = resposta.json()
    return {
        "nome": dados["name"],
        "calorias": dados["nutritions"]["calories"],
        "acucar": dados["nutritions"]["sugar"],
    }


def calcular_totais(frutas):
    
    total_calorias = 0
    total_acucar = 0
    for nome in frutas:
        fruta = buscar_fruta(nome)
        total_calorias += fruta["calorias"]
        total_acucar += fruta["acucar"]
    return round(total_calorias, 1), round(total_acucar, 1)



@app.get("/frutas/<nome>")
def consultar_fruta(nome):
    return jsonify(buscar_fruta(nome))


@app.post("/sucos")
def cadastrar_suco():
    global proximo_id
    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    frutas = dados.get("frutas")
    tem_gosto_de = dados.get("tem_gosto_de")

    if not nome or not isinstance(frutas, list) or not frutas or not tem_gosto_de:
        return jsonify({"erro": "Envie 'nome', 'frutas' (lista) e 'tem_gosto_de'."}), 400

    calorias, acucar = calcular_totais(frutas)

    suco = {
        "id": proximo_id,
        "nome": nome,
        "frutas": frutas,
        "tem_gosto_de": tem_gosto_de,
        "total_calorias": calorias,
        "total_acucar": acucar,
    }
    sucos.append(suco)
    proximo_id += 1

    return jsonify(suco), 201


@app.get("/sucos")
def listar_sucos():
    return jsonify(sucos)



@app.put("/sucos/<int:id>")
def atualizar_suco(id):
    dados = request.get_json(silent=True) or {}
    frutas = dados.get("frutas")

    if not isinstance(frutas, list) or not frutas:
        return jsonify({"erro": "Envie 'frutas' como uma lista."}), 400

    for suco in sucos:
        if suco["id"] == id:
            calorias, acucar = calcular_totais(frutas)
            suco["frutas"] = frutas
            suco["total_calorias"] = calorias
            suco["total_acucar"] = acucar
            return jsonify(suco)

    return jsonify({"erro": f"Suco {id} não encontrado."}), 404


if __name__ == "__main__":
    app.run(debug=True)