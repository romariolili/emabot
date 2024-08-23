# -*- coding: utf-8 -*-
"""emma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15YsDsyz4O2f8ZRb0WDs_4iQUYaPpnzvj
"""
from flask import Flask, request, render_template_string, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessário para usar sessões

# Caminho do arquivo no servidor
file_path = 'teste 1.xlsx'

# Verifica se o arquivo existe
if os.path.exists(file_path):
    # Carregar a planilha Excel
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=["Palavras chaves", "Título do documento", "Link Qualyteam", "Resumo"])

# Emoji de rosto humano
face_emoji = "😊"

# Função para inicializar o histórico de chat
def initialize_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = [
            "🤖 Emabot: Olá, me chamo Emaboot da Diplan. Sou sua assistente de busca de documentos. Como posso ajudar? Fale comigo somente por palavras-chave. Exemplo: Processos.."
        ]
    return session['chat_history']

# Função para adicionar mensagem ao histórico de chat
def add_to_chat_history(message):
    chat_history = session.get('chat_history', [])
    chat_history.append(message)
    session['chat_history'] = chat_history

# Função de busca na planilha
def search_in_spreadsheet(term):
    results = df[df['Palavras chaves'].str.contains(fr'\b{term}\b', case=False, na=False, regex=True)]
    if not results.empty:
        return results[['Título do documento', 'Link Qualyteam', 'Resumo']].to_dict('records')
    else:
        return []

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def home():
    chat_history = initialize_chat_history()

    if request.method == 'POST':
        user_input = request.form['user_input'].strip()

        if user_input:
            if len(user_input.split()) > 1:
                add_to_chat_history(f"{face_emoji}: {user_input}")
                add_to_chat_history("🤖 Emabot: Só consigo realizar a busca por uma única palavra-chave.")
            elif len(user_input) < 3:
                add_to_chat_history(f"{face_emoji}: {user_input}")
                add_to_chat_history("🤖 Emabot: A busca deve conter pelo menos 3 caracteres.")
            else:
                add_to_chat_history(f"{face_emoji}: {user_input}")
                results = search_in_spreadsheet(user_input)
                if results:
                    add_to_chat_history("🤖 Emabot: Documentos encontrados:")
                    for result in results:
                        add_to_chat_history(f"📄 <a href='/get_link?title={result['Título do documento']}'> {result['Título do documento']}</a>")
                else:
                    add_to_chat_history("🤖 Emabot: Nenhum documento encontrado com essa palavra-chave.")
        else:
            add_to_chat_history("🤖 Emabot: Por favor, insira uma palavra-chave para realizar a busca.")

    return render_template_string(template, chat_history=session['chat_history'])

# Rota para obter o link do documento
@app.route('/get_link', methods=['GET'])
def get_link():
    title = request.args.get('title')
    result = df[df['Título do documento'] == title]
    if not result.empty:
        link = result['Link Qualyteam'].values[0]
        resumo = result['Resumo'].values[0]
        add_to_chat_history(f"🤖 Emabot: Aqui está o link para '{title}': <a href='{link}' target='_blank'>{link}</a>")
        add_to_chat_history(f"📄 Resumo: {resumo}")
    else:
        add_to_chat_history("🤖 Emabot: Link não encontrado para o título selecionado.")

    return render_template_string(template, chat_history=session['chat_history'])

# Template HTML com JavaScript e CSS adicionados
template = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emabot da Diplan</title>
    <style>
        /* Estilos para o indicador de carregamento */
        #loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.8);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            font-size: 1.5em;
            color: #333;
        }
        /* Animação de rotação */
        @keyframes spin {
            from {transform: rotate(0deg);}
            to {transform: rotate(360deg);}
        }
        .spinner {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        /* Estilos gerais */
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            margin: 0;
            padding: 20px;
        }
        .container {
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
        }
        .chat-box {
            width: 70%;
            margin-right: 20px;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-history {
            border:1px solid #ccc;
            padding:10px;
            height: 400px;
            overflow-y: auto;
            margin-bottom:10px;
            border-radius: 4px;
            background-color: #fafafa;
        }
        .chat-history p {
            margin: 5px 0;
        }
        .user-input {
            display: flex;
            align-items: center;
        }
        .user-input input[type="text"] {
            width: 100%;
            padding: 10px;
            border:1px solid #ccc;
            border-radius: 4px;
            font-size: 1em;
        }
        .user-input input[type="submit"] {
            padding: 10px 20px;
            margin-left: 10px;
            border:none;
            background-color: #3498db;
            color: #fff;
            border-radius: 4px;
            font-size: 1em;
            cursor: pointer;
        }
        .user-input input[type="submit"]:hover {
            background-color: #2980b9;
        }
        .image-box {
            width: 30%;
            text-align: center;
        }
        .image-box img {
            width: 100%;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div id="loading-overlay">
        <div class="spinner"></div>
        <div>Analisando...</div>
    </div>

    <div class="container">
        <div class="chat-box">
            <h1>Emabot da Diplan</h1>
            <div class="chat-history">
                {% for message in chat_history %}
                    <p>{{ message | safe }}</p>
                {% endfor %}
            </div>
            <form method="post" action="/" onsubmit="showLoading()">
                <div class="user-input">
                    <input type="text" id="user_input" name="user_input" placeholder="Digite sua palavra-chave aqui...">
                    <input type="submit" value="Enviar">
                </div>
            </form>
        </div>
        <div class="image-box">
            <img src="/static/images/your_image_name.png" alt="Diplan Assistant">
        </div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('loading-overlay').style.display = 'flex';
        }
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)
