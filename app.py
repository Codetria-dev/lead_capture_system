from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import db, Lead
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-altere-em-producao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Credenciais administrativas (hardcoded para demonstração)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'


def login_required(f):
    """Decorator para proteger rotas administrativas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Criar tabelas ao iniciar
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Landing page com formulário de captação"""
    return render_template('index.html')


@app.route('/cadastrar', methods=['POST'])
def cadastrar_lead():
    """Processa o formulário e salva o lead no banco"""
    try:
        # Validar dados obrigatórios
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        empresa = request.form.get('empresa', '').strip()
        mensagem = request.form.get('mensagem', '').strip()
        
        # Validações básicas
        if not nome:
            flash('O nome é obrigatório.', 'error')
            return redirect(url_for('index'))
        
        if not email:
            flash('O e-mail é obrigatório.', 'error')
            return redirect(url_for('index'))
        
        if not telefone:
            flash('O telefone é obrigatório.', 'error')
            return redirect(url_for('index'))
        
        # Verificar se já existe lead com mesmo email
        lead_existente = Lead.query.filter_by(email=email).first()
        if lead_existente:
            flash('Este e-mail já está cadastrado.', 'error')
            return redirect(url_for('index'))
        
        # Criar novo lead
        novo_lead = Lead(
            nome=nome,
            email=email,
            telefone=telefone,
            empresa=empresa if empresa else None,
            mensagem=mensagem if mensagem else None
        )
        
        db.session.add(novo_lead)
        db.session.commit()
        
        return redirect(url_for('sucesso', lead_id=novo_lead.id))
    
    except Exception as e:
        db.session.rollback()
        flash('Erro ao cadastrar lead. Tente novamente.', 'error')
        return redirect(url_for('index'))


@app.route('/sucesso/<int:lead_id>')
def sucesso(lead_id):
    """Página de sucesso após cadastro"""
    lead = Lead.query.get_or_404(lead_id)
    return render_template('sucesso.html', lead=lead)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login administrativo"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'error')
    
    # Se já estiver logado, redireciona para dashboard
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout do sistema administrativo"""
    session.pop('logged_in', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard com lista de leads paginada"""
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Leads por página
    
    # Query ordenada por data (mais recentes primeiro)
    leads_query = Lead.query.order_by(Lead.data_cadastro.desc())
    
    # Paginação
    pagination = leads_query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    leads = pagination.items
    
    return render_template('dashboard.html', 
                         leads=leads, 
                         pagination=pagination)


@app.route('/lead/<int:lead_id>')
@login_required
def detalhes_lead(lead_id):
    """Página de detalhes do lead"""
    lead = Lead.query.get_or_404(lead_id)
    return render_template('detalhes.html', lead=lead)


@app.route('/lead/<int:lead_id>/excluir', methods=['POST'])
@login_required
def excluir_lead(lead_id):
    """Exclui um lead"""
    lead = Lead.query.get_or_404(lead_id)
    
    try:
        db.session.delete(lead)
        db.session.commit()
        flash('Lead excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir lead.', 'error')
    
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
