# -*- coding: utf-8 -*-
"""emma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15YsDsyz4O2f8ZRb0WDs_4iQUYaPpnzvj
"""
import os
from flask import Flask, request, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Caminho do arquivo no servidor
file_path = 'teste 1.xlsx'

# Carregar a planilha Excel
df = pd.read_excel(file_path)

def search_in_spreadsheet(term):
    results = df[df['Palavras chaves'].str.contains(term, case=False, na=False)]
    if not results.empty:
        return results[['Título do documento', 'Link Qualyteam']].to_dict('records')
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        term = request.form['search']
        results = search_in_spreadsheet(term)
        if results:
            return render_template_string('''
                <h1>Emaboot Chatbot</h1>
                <p><b>🤖 Emaboot:</b> Documentos encontrados:</p>
                <ul>
                {% for result in results %}
                    <li><a href="/get_link?title={{ result['Título do documento'] }}">{{ result['Título do documento'] }}</a></li>
                {% endfor %}
                </ul>
                <br><a href="/">Voltar</a>
            ''', results=results)
        else:
            return render_template_string('''
                <h1>Emaboot Chatbot</h1>
                <p><b>🤖 Emaboot:</b> Nenhum documento encontrado com essas palavras-chave.</p>
                <br><a href="/">Voltar</a>
            ''')
    return render_template_string('''
        <h1>Emaboot Chatbot</h1>
        <form method="post">
            <label for="search">🤖 Emaboot: Qual documento procura hoje?</label><br><br>
            <input type="text" id="search" name="search">
            <input type="submit" value="Enviar">
        </form>
    ''')

@app.route('/get_link', methods=['GET'])
def get_link():
    title = request.args.get('title')
    result = df[df['Título do documento'] == title]
    if not result.empty:
        link = result['Link Qualyteam'].values[0]
        return render_template_string('''
            <h1>Emaboot Chatbot</h1>
            <p><b>🤖 Emaboot:</b> Aqui está o link para '{{ title }}':</p>
            <a href="{{ link }}" target="_blank">{{ link }}</a>
            <br><br><a href="/">Voltar</a>
        ''', title=title, link=link)
    else:
        return render_template_string('''
            <h1>Emaboot Chatbot</h1>
            <p><b>🤖 Emaboot:</b> Link não encontrado para o título selecionado.</p>
            <br><a href="/">Voltar</a>
        ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
