from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

projetos = []
pasta_projetos = 'projetos'
os.makedirs(pasta_projetos, exist_ok=True)

@app.route('/')
def index():
    dados = {
        'metrica1': 75,
        'metrica2': 120,
        'metrica3': 50,
        'projetos': listar_projetos()
    }
    return render_template('dashboard.html', dados=dados)

@app.route('/criar_projeto', methods=['POST'])
def criar_projeto():
    global projetos

    nome_projeto = request.form.get('nome_projeto')

    if nome_projeto:
        projetos.append({'nome': nome_projeto})

        caminho_pasta_projeto = os.path.join(pasta_projetos, nome_projeto)
        os.makedirs(caminho_pasta_projeto, exist_ok=True)

        os.makedirs(os.path.join(caminho_pasta_projeto, 'Documentação SST'), exist_ok=True)
        os.makedirs(os.path.join(caminho_pasta_projeto, 'Colaboradores'), exist_ok=True)

        caminho_info_projeto = os.path.join(caminho_pasta_projeto, 'info.txt')
        with open(caminho_info_projeto, 'w') as arquivo_info:
            arquivo_info.write(f'Nome do Projeto: {nome_projeto}')

        return redirect(url_for('upload_arquivos', nome_projeto=nome_projeto, _method='POST'))

    return render_template('criacao_novo_projeto.html', nome_projeto=nome_projeto)

@app.route('/upload_arquivos/<nome_projeto>', methods=['GET', 'POST'])
def upload_arquivos(nome_projeto):
    if request.method == 'POST':
        caminho_pasta_projeto = os.path.join(pasta_projetos, nome_projeto)

        # Obtenha os arquivos de cada campo de upload
        arquivos_sst = request.files.getlist('arquivos_sst')
        arquivos_colaboradores = request.files.getlist('arquivos_colaboradores')

        # Salve os arquivos nas pastas do projeto
        for arquivo in arquivos_sst:
            if arquivo:
                caminho_arquivo_sst = os.path.join(caminho_pasta_projeto, 'Documentação SST', secure_filename(arquivo.filename))
                arquivo.save(caminho_arquivo_sst)

        for arquivo in arquivos_colaboradores:
            if arquivo:
                caminho_arquivo_colaboradores = os.path.join(caminho_pasta_projeto, 'Colaboradores', secure_filename(arquivo.filename))
                arquivo.save(caminho_arquivo_colaboradores)
                
    return render_template('upload_arquivos.html', nome_projeto=nome_projeto, url_upload_arquivos=request.path)

@app.route('/ver_projeto/<nome_projeto>')
def ver_projeto(nome_projeto):
    caminho_pasta_projeto = os.path.join(pasta_projetos, nome_projeto)
    caminho_documentacao_sst = os.path.join(caminho_pasta_projeto, 'Documentação SST')
    caminho_colaboradores = os.path.join(caminho_pasta_projeto, 'Colaboradores')

    # Obtém a lista de arquivos para Documentação SST
    lista_documentacao_sst = [f for f in os.listdir(caminho_documentacao_sst) if os.path.isfile(os.path.join(caminho_documentacao_sst, f))]

    # Obtém a lista de arquivos para Colaboradores
    lista_colaboradores = [f for f in os.listdir(caminho_colaboradores) if os.path.isfile(os.path.join(caminho_colaboradores, f))]

    return render_template('ver_projeto.html', nome_projeto=nome_projeto, lista_documentacao_sst=lista_documentacao_sst, lista_colaboradores=lista_colaboradores)

@app.route('/projetos/<nome_projeto>/<pasta>/<path:nome_arquivo>')
def servir_arquivo(nome_projeto, pasta, nome_arquivo):
    caminho_pasta_projeto = os.path.join(pasta_projetos, nome_projeto, pasta)
    return send_from_directory(caminho_pasta_projeto, nome_arquivo)

def listar_projetos():
    return [{'nome': projeto} for projeto in os.listdir(pasta_projetos) if os.path.isdir(os.path.join(pasta_projetos, projeto))]

if __name__ == '__main__':
    app.run(debug=True)
