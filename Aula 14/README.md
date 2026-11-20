# API Casa de Sucos

API feita em **Python** e **Flask** para uma Casa de Sucos. Ela usa a API pública **Fruityvice** (`https://www.fruityvice.com/api/fruit`) para buscar as calorias e o açúcar das frutas e calcular os valores de cada suco (considerando **100 g** de cada fruta).

## Funcionalidades

- **`GET /frutas/<nome>`**: Busca uma fruta na Fruityvice e mostra só o `nome`, as `calorias` e o `acucar`.
- **`POST /sucos`**: Cadastra um suco (`nome`, `frutas`, `tem_gosto_de`), soma as calorias e o açúcar das frutas e guarda o suco.
- **`GET /sucos`**: Mostra todos os sucos cadastrados com os valores nutricionais.
- **`PUT /sucos/<id>`** *(Desafio bônus)*: Troca as frutas de um suco e recalcula os valores.
- **Tratamento de erros**: Se a fruta ou o suco não existir, retorna erro `404` com uma mensagem. Se faltar algum campo no cadastro retorna `400`, e se a Fruityvice estiver fora do ar retorna `503`.

## Instalação

1. **Abra a pasta do projeto no terminal.**

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate
   ```

3. **Instale as bibliotecas:**
   ```bash
   python -m pip install -r requirements.txt
   ```

## Como executar

Com o ambiente virtual ativado, rode:

```bash
python app.py
```

A API fica disponível em `http://127.0.0.1:5000`.

> **Observação:** Os sucos ficam guardados só na memória, então quando o servidor é reiniciado a lista zera. Os nomes das frutas precisam ser em inglês (ex: `banana`, `strawberry`), porque a Fruityvice não aceita em português.
