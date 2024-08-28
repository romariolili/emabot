# -*- coding: utf-8 -*-
"""emma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15YsDsyz4O2f8ZRb0WDs_4iQUYaPpnzvj
"""
from flask import Flask, request, render_template_string, redirect, url_for
import pandas as pd
import os
from unidecode import unidecode

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

# Função para normalizar o texto, removendo acentuação e convertendo para minúsculas
def normalize(text):
    return unidecode(text.strip().lower())

# Função de busca na planilha
def search_in_spreadsheet(term):
    normalized_term = normalize(term)
    possible_terms = [normalized_term, normalized_term + 's', normalized_term.rstrip('s')]

    # Busca tanto na coluna "Palavras chaves" quanto na coluna "Resumo"
    results = df[df.apply(lambda row: any(
        normalize(word) in possible_terms for word in str(row['Palavras chaves']).split(';')
    ) or normalized_term in normalize(row['Resumo']), axis=1)]

    if not results.empty:
        return results[['Título do documento', 'Link Qualyteam', 'Resumo']].to_dict('records')
    else:
        return []

# Função para inicializar o histórico de chat
def initialize_chat_history():
    return [
        "🤖 Emabot: Olá, me chamo Emaboot da Diplan. Sou sua assistente de busca de documentos. Como posso ajudar? Digite uma palavra-chave ou uma frase."
    ]

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def home():
    # Inicializa o histórico de chat sempre que a página for carregada/recarregada
    chat_history = initialize_chat_history()

    if request.method == 'POST':
        user_input = request.form['user_input'].strip()

        if user_input:
            chat_history.append(f"{face_emoji}: {user_input}")
            results = search_in_spreadsheet(user_input)
            if results:
                chat_history.append("🤖 Emabot: Documentos encontrados:")
                for result in results:
                    chat_history.append(f"📄 <a href='/get_link?title={result['Título do documento']}'>{result['Título do documento']}</a>")
            else:
                chat_history.append("🤖 Emabot: Nenhum documento encontrado com o termo ou frase fornecida.")
        else:
            chat_history.append("🤖 Emabot: Por favor, insira uma palavra-chave ou frase para realizar a busca.")

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
        chat_history.append(f"📄 Resumo: {resumo} <button onclick='speakText(`{resumo}`)'>🔊 Ouvir</button>")
    else:
        chat_history.append("🤖 Emabot: Link não encontrado para o título selecionado.")

    return render_template_string(template, chat_history=chat_history)

# Template HTML com a imagem de fundo, VLibras e Text-to-Speech adicionados
template = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emabot da Diplan</title>

    <!-- Script do VLibras -->
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>
        new window.VLibras.Widget('https://vlibras.gov.br/app');
    </script>

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
            align-items: center;
            box-sizing: border-box;
        }
        /* Container principal */
        .container {
            display: flex;
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 20px;
            justify-content: flex-start;
            flex-direction: column;
            height: 100%;
            box-sizing: border-box;
        }
        /* Caixa de Chat - Versão Desktop */
        .chat-box {
            width: 100%;
            max-width: 600px; /* Volta a configuração anterior para desktop */
            background-color: rgba(0, 0, 51, 0.8);
            padding: 20px;
            border-radius: 8px;
            box-sizing: border-box;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            align-self: flex-start;
            margin-top: 10%;
            height: auto;
            max-height: 70vh;
        }
        /* Estilos para histórico de chat */
        .chat-history {
            border: 1px solid #ccc;
            padding: 10px;
            height: auto;
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 10px;
            border-radius: 4px;
            background-color: rgba(255, 255, 255, 0.1);
            box-sizing: border-box;
        }
        /* Texto do histórico */
        .chat-history p {
            margin: 5px 0;
            color: white;
            word-wrap: break-word; /* Garante que o texto seja quebrado corretamente */
        }
        /* Campo de entrada e botão de envio */
        .user-input {
            display: flex;
            align-items: center;
            width: 100%;
            box-sizing: border-box;
        }
        .user-input input[type="text"] {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1em;
            color: black;
            box-sizing: border-box;
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
            box-sizing: border-box;
        }
        .user-input input[type="submit"]:hover {
            background-color: #2980b9;
        }
        /* Estilos para links */
        a {
            color: white;
            text-decoration: underline;
        }
        a:hover {
            color: #ccc;
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
        /* Ajustes para versão mobile */
        @media screen and (max-width: 768px) {
            .chat-box {
                width: 50%; /* Ajusta a largura para 50% da tela em dispositivos móveis */
                max-width: 300px; /* Limita a largura máxima da caixa em dispositivos móveis */
                margin-top: 5%;
                max-height: 80vh;
            }

            .chat-history p {
                font-size: 0.9em; /* Reduz o tamanho da fonte na versão mobile */
            }

            .user-input {
                flex-direction: column;
            }

            .user-input input[type="text"] {
                font-size: 0.9em; /* Reduz o tamanho da fonte na versão mobile */
            }

            .user-input input[type="submit"] {
                margin-left: 0;
                margin-top: 10px;
                width: 100%;
                font-size: 0.9em; /* Reduz o tamanho da fonte na versão mobile */
            }

            .chat-history {
                max-height: 250px;
            }
        }
    </style>
</head>
<body>
    <!-- Inclui o Plugin do VLibras -->
    <div vw class="enabled">
        <div vw-access-button class="active"></div>
        <div vw-plugin-wrapper>
            <div class="vw-plugin-top-wrapper"></div>
        </div>
    </div>

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
                    <input type="text" id="user_input" name="user_input" placeholder="Digite sua palavra-chave ou frase aqui...">
                    <input type="submit" value="Enviar">
                </div>
            </form>
        </div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('loading-overlay').style.display = 'flex';
        }

        function speakText(text) {
            if ('speechSynthesis' in window) {  // Verifica se o navegador suporta a API
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'pt-BR';  // Define o idioma para Português
                speechSynthesis.speak(utterance);
            } else {
                alert("Seu navegador não suporta a API de síntese de fala.");
            }
        }
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)
