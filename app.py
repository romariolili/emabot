# -*- coding: utf-8 -*-
"""emma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15YsDsyz4O2f8ZRb0WDs_4iQUYaPpnzvj
"""
from flask import Flask, request, render_template_string
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
    df = pd.DataFrame(columns=["Palavras chaves", "Título do documento", "Link Qualyteam"])

# Emoji de rosto humano
face_emoji = "👤"

# Inicializa o histórico de chat como uma variável global
chat_history = []

def search_in_spreadsheet(term):
    results = df[df['Palavras chaves'].str.contains(term, case=False, na=False)]
    if not results.empty:
        return results[['Título do documento', 'Link Qualyteam']].to_dict('records')
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    global chat_history  # Acessa a variável global chat_history
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # Substitui o texto do usuário pelo emoji de rosto humano
        user_message = f"{face_emoji}: {user_input}"
        chat_history.append(user_message)
        
        results = search_in_spreadsheet(user_input)
        if results:
            chat_history.append("🤖 Emabot: Documentos encontrados:")
            for result in results:
                chat_history.append(f"📄 <a href='/get_link?title={result['Título do documento']}'>{result['Título do documento']}</a>")
        else:
            chat_history.append("🤖 Emabot: Nenhum documento encontrado com essas palavras-chave.")
    
    return render_template_string('''
        <h1>Emabot da Diplan</h1>
        <div style="border:1px solid #ccc; padding:10px; height:300px; overflow-y:scroll; margin-bottom:10px;">
            {% for message in chat_history %}
                <p>{{ message | safe }}</p>
            {% endfor %}
        </div>
        <form method="post">
            <label for="user_input">Digite sua mensagem:</label><br>
            <input type="text" id="user_input" name="user_input" style="width:80%">
            <input type="submit" value="Enviar">
        </form>
    ''', chat_history=chat_history)

@app.route('/get_link', methods=['GET'])
def get_link():
    global chat_history  # Acessa a variável global chat_history
    title = request.args.get('title')
    result = df[df['Título do documento'] == title]
    if not result.empty:
        link = result['Link Qualyteam'].values[0]
        chat_history.append(f"🤖 Emabot: Aqui está o link para '{title}': <a href='{link}' target='_blank'>{link}</a>")
        return home()
    else:
        return render_template_string('''
            <h1>Emabot da Diplan</h1>
            <p><b>🤖 Emabot:</b> Link não encontrado para o título selecionado.</p>
            <br><a href="/">Voltar</a>
        ''')

if __name__ == "__main__":
    # Inicializa a conversa com a nova saudação
    chat_history.append("🤖 Emabot: Olá, eu sou a Emabot da Diplan. Sou seu assistente de busca... Como posso ajudar?")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
