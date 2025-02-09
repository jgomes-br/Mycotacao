# MyCotacao

## 📌 Visão Geral
**MyCotacao** é um web app desenvolvido em Python com Django para auxiliar na gestão de cotações de produtos. O objetivo principal do projeto é fornecer uma plataforma eficiente para fazer contações entre compradores e vendedores, em um formato de leilão.


## 🚀 Funcionalidades
- 📊 **Cadastro de produtos**: Permite o registro de novos produtos para cotação.
- 📊 **Cadastro de Fornecedores e Compradores**: Permite o registro de novos produtos para cotação.
- 🔍 **Consulta de preços**: Verificação e comparação de preços cadastrados.
- 📅 **Histórico de cotações**: Acompanhamento da evolução dos preços.
- 👤 **Autenticação de usuários**: Controle de acesso com login e senha.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10
- **Banco de Dados:** SQLite
- **Frontend:** HTML, CSS, JavaScript, Angular
- **Bibliotecas:** Django 4.0, openpyxl

## 📁 Estrutura do Projeto
```
MyCotacao/
│── mycotacao/        # Aplicação principal do Django
│── scripts/          # Scripts auxiliares
│── wireframe/        # Protótipos e esboços do sistema
│── requirements.txt  # Dependências do projeto
│── manage.py         # Gerenciador do Django
```

## 🏗️ Como Configurar e Rodar o Projeto
### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/jgomes-br/Mycotacao.git
cd Mycotacao
```
### 2️⃣ Criar um Ambiente Virtual e Instalar Dependências
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3️⃣ Aplicar Migrações e Criar Superusuário
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4️⃣ Rodar o Servidor
```bash
python manage.py runserver
```
Acesse o sistema em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📌 Contribuição
Se quiser contribuir com melhorias, siga estas etapas:
1. Faça um fork do repositório.
2. Crie uma branch (`git checkout -b minha-branch`).
3. Realize as alterações e faça commits (`git commit -m 'Minha melhoria'`).
4. Envie um pull request.

## 📜 Licença
Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

📧 **Contato:** joao.09.05@gmail.com (ou outro contato preferido).

