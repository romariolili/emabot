# -*- coding: utf-8 -*-
"""emma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15YsDsyz4O2f8ZRb0WDs_4iQUYaPpnzvj
"""
from flask import Flask, request, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Caminho do arquivo no sistema de arquivos do Render (ou no seu ambiente local)
file_path = 'teste 1.xlsx'

# Carregar a planilha Excel
df = pd.read_excel(file_path)

def search_in_spreadsheet(term):
    results = df[df['Palavras chaves'].str.contains(term, case=False, na=False)]
    if not results.empty:
        return results['Título do documento'].tolist()
    else:
        return []

def get_link_by_title(title):
    result = df[df['Título do documento'] == title]
    if not result.empty:
        return result['Link Qualyteam'].values[0]
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_interaction():
    user_input = request.form.get("input")
    
    if user_input.lower() in ["sair", "exit", "quit"]:
        return render_template('index.html', response="🤖 Emaboot: Até logo!")
    
    term = user_input
    results = search_in_spreadsheet(term)
    
    if results:
        response = "🤖 Emaboot: Documentos encontrados:<br>"
        for i, title in enumerate(results, 1):
            response += f"<a href='/get_link?title={title}'>{i}. {title}</a><br>"
        return render_template('index.html', response=response)
    else:
        return render_template('index.html', response="🤖 Emaboot: Nenhum documento encontrado com essas palavras-chave.")

@app.route('/get_link')
def get_link():
    title = request.args.get("title")
    link = get_link_by_title(title)
    
    if link:
        return render_template('index.html', response=f"🤖 Emaboot: Aqui está o link para '{title}': <a href='{link}' target='_blank'>{link}</a>")
    else:
        return render_template('index.html', response="🤖 Emaboot: Link não encontrado para o título selecionado.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

