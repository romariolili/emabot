# -*- coding: utf-8 -*-
"""emma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15YsDsyz4O2f8ZRb0WDs_4iQUYaPpnzvj
"""
from flask import Flask, request, render_template_string, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

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
    return [
        "🤖 Emabot: Olá, me chamo Emaboot da Diplan. Sou sua assistente de busca de documentos. Como posso ajudar? Fale comigo somente por palavras-chave. Exemplo: Processos.."
    ]

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
    # Inicializa o histórico de chat sempre que a página for carregada/recarregada
    chat_history = initialize_chat_history()

    if request.method == 'POST':
        user_input = request.form['user_input'].strip()

        if user_input:
            if len(user_input.split()) > 1:
                chat_history.append(f"{face_emoji}: {user_input}")
                chat_history.append("🤖 Emabot: Só consigo realizar a busca por uma única palavra-chave.")
            elif len(user_input) < 3:
                chat_history.append(f"{face_emoji}: {user_input}")
                chat_history.append("🤖 Emabot: A busca deve conter pelo menos 3 caracteres.")
            else:
                chat_history.append(f"{face_emoji}: {user_input}")
                results = search_in_spreadsheet(user_input)
                if results:
                    chat_history.append("🤖 Emabot: Documentos encontrados:")
                    for result in results:
                        chat_history.append(f"📄 <a href='/get_link?title={result['Título do documento']}'>{result['Título do documento']}</a>")
                else:
                    chat_history.append("🤖 Emabot: Nenhum documento encontrado com essa palavra-chave.")
        else:
            chat_history.append("🤖 Emabot: Por favor, insira uma palavra-chave para realizar a busca.")

    return render_template_string(template, chat_history=chat_history)

# Rota para obter o link do documento
@app.route('/get_link', methods=['GET'])
def get_link():
    title = request.args.get('title')
    result = df[df['Título do documento'] == title]
    chat_history = initialize_chat_history()
    if not result.empty:
        link = result['Link Qualyteam'].values[0]
        resumo = result['Resumo'].values[0]
        chat_history.append(f"🤖 Emabot: Aqui está o link para '{title}': <a href='{link}' target='_blank'>{link}</a>")
        chat_history.append(f"📄 Resumo: {resumo}")
    else:
        chat_history.append("🤖 Emabot: Link não encontrado para o título selecionado.")

    return render_template_string(template, chat_history=chat_history)

# Template HTML com a imagem de fundo e estilos adicionados
template = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emabot da Diplan</title>
    <style>
        /* Estilos gerais */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-image: url('/static/images/Imagem de fundo.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: white;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-end; /* Alinha o conteúdo na parte inferior da página */
        }
        .container {
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            justify-content: flex-start; /* Alinhamento à esquerda */
            flex-direction: column;
            margin-top: 100px; /* Reduz a margem superior para subir a caixa */
        }
        .chat-box {
            width: 50%;
            background-color: rgba(0, 0, 51, 0.8); /* Fundo da caixa de chat com transparência */
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-left: 0; /* Alinhado à esquerda */
        }
        .chat-history {
            border: 1px solid #ccc;
            padding: 10px;
            height: 256px; /* Reduzido em mais 15% da altura anterior de 320px */
            overflow-y: auto;
            margin-bottom: 10px;
            border-radius: 4px;
            background-color: rgba(255, 255, 255, 0.1); /* Fundo da caixa de histórico com transparência */
        }
        .chat-history p {
            margin: 5px 0;
            color: white; /* Garante que o texto fique sempre branco */
        }
        .user-input {
            display: flex;
            align-items: center;
        }
        .user-input input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1em;
            color: black;
        }
        .user-input input[type="submit"] {
            padding: 10px 20px;
            margin-left: 10px;
            border: none;
            background-color: #3498db;
            color: #fff;
            border-radius: 4px;
            font-size: 1em;
            cursor: pointer;
        }
        .user-input input[type="submit"]:hover {
            background-color: #2980b9;
        }
        /* Estilos para links */
        a {
            color: white; /* Links em branco */
            text-decoration: underline;
        }
        a:hover {
            color: #ccc; /* Cor dos links ao passar o mouse */
        }
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
