from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from auth_decorator import login_required, setor_required
from crud import create_point, create_user, get_all_points, get_point_by_id, get_user_by_email, get_user_by_id, update_user, log_login_attempt, get_all_users
import bcrypt
import re

load_dotenv()

# Criando um Blueprint
user_routes = Blueprint('user_routes', __name__)

############################# Criar  #############################

@user_routes.route('/create_user', methods=['GET', 'POST'])
def create_user_route():
    if request.method == 'GET':
        # Lógica para renderizar o formulário
        return render_template('create_user.html')
    
    elif request.method == 'POST':
        try:
            # Coletando dados do formulário
            email = request.form['email']
            password = request.form['password']
            first_name = request.form['first_name']
            nascimento = request.form['nascimento']
            celular = request.form['celular']
            bairro = request.form['bairro']
            cidade = request.form['cidade']

            # Chamando a função de criação de usuário
            create_user(email, password, first_name, nascimento, celular, bairro, cidade)

            # Mensagem de sucesso
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('user_routes.create_user_route'))

        except ValueError as ve:
            flash(str(ve), 'error')
            return redirect(url_for('user_routes.create_user_route'))
        except Exception as e:
            flash(f'Erro ao criar o usuário: {str(e)}', 'error')
            return redirect(url_for('user_routes.create_user_route'))


@user_routes.route('/create_point', methods=['GET', 'POST'])
def create_point_route():
    if request.method == 'GET':
        # Lógica para renderizar o formulário
        return render_template('create_point.html')
    
    elif request.method == 'POST':
        try:
            # Coletando dados do formulário
            nome = request.form['nome']
            categoria = request.form['categoria']
            endereco = request.form['endereco']
            acessibilidade = request.form['acessibilidade']
            custos = request.form['custos']
            estacoes = request.form['estacoes']
            cidade = request.form['cidade']
            bairro = request.form['bairro']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            # Chamando a função de criação de usuário
            create_point(nome, categoria, endereco, acessibilidade, custos, estacoes, cidade, bairro, latitude, longitude)

            # Mensagem de sucesso
            flash('Point criado com sucesso!', 'success')
            return redirect(url_for('user_routes.create_point_route'))

        except ValueError as ve:
            flash(str(ve), 'error')
            return redirect(url_for('user_routes.create_point_route'))
        except Exception as e:
            flash(f'Erro ao criar o point: {str(e)}', 'error')
            return redirect(url_for('user_routes.create_point_route'))

############################# Login #############################
# @user_routes.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')

#     elif request.method == 'POST':
#         try:
#             SECRET_KEY = os.getenv('SECRET_KEY_TOKEN')
#             URL_login = os.getenv('URL_login')
#             DOMINIO_COOKIE = os.getenv('DOMINIO_COOKIE')

#             email = request.form['email']
#             password = request.form['password']

#             # Pegar o endereço IP do usuário
#             ip_address = request.remote_addr

#             # Verificação de e-mail inválido
#             email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#             if not re.match(email_regex, email):
#                 flash('E-mail inválido.', 'error')
#                 return render_template('login.html')

#             # Utilizando função do CRUD para buscar o usuário
#             user = get_user_by_email(email)
#             if not user:
#                 flash('Usuário não cadastrado.', 'error')
#                 return render_template('login.html')

#             # Verificar se a senha está correta
#             if password == user['password_hash']:
#                 token = jwt.encode({
#                     'user_id': str(user['_id']),
#                     'exp': datetime.now(timezone.utc) + timedelta(hours=20)
#                 }, SECRET_KEY, algorithm='HS256')

#                 # Atualiza o token de login no banco de dados
#                 update_user(user['_id'], {'login_token': token})

#                 # Registra a tentativa de login bem-sucedida
#                 log_login_attempt(user['_id'], "success", ip_address)

#                 # Cria a resposta e define o token no cookie
#                 response = redirect(url_for('user_routes.dashboard'))
#                 response.set_cookie('token', token, max_age=60*60*20, httponly=True,
#                                     secure=False, samesite='Lax', domain=DOMINIO_COOKIE, path='/')
#                 return response
#             else:
#                 # Registra a tentativa de login com falha
#                 log_login_attempt(user['_id'], "failure", ip_address)

#                 #Retorna mensagem de login com falha
#                 flash('Credenciais inválidas.', 'error')
#                 return render_template('login.html')
#         except Exception as e:
#             print(f"Erro no login: {e}")
#             flash('Erro ao tentar fazer login. Tente novamente mais tarde.', 'error')
#             return render_template('login.html')


@user_routes.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    try:
        SECRET_KEY = os.getenv('SECRET_KEY_TOKEN')
        token = request.cookies.get('token')
        if not token:
            flash('Você precisa estar logado para acessar esta página.', 'error')
            return redirect(url_for('user_routes.login'))

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')

        # Utilizando função do CRUD para buscar o usuário
        current_user = get_user_by_id(user_id)
        if not current_user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('user_routes.login'))

        if request.method == 'GET':
            return render_template('edit_profile.html', user=current_user, current_user=current_user)

        elif request.method == 'POST':
            email = request.form['email']
            password = request.form.get('password', None)
            first_name = request.form['first_name']
            last_name = request.form['last_name']

            if email != current_user['email']:
                existing_user = get_user_by_email(email)
                if existing_user and existing_user['_id'] != current_user['_id']:
                    flash('Este e-mail já está cadastrado.', 'error')
                    return redirect(url_for('user_routes.edit_profile'))

            update_fields = {
                "email": email,
                "profile.first_name": first_name,
                "profile.last_name": last_name
            }

            if password:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                update_fields['password_hash'] = password_hash.decode('utf-8')

            update_user(current_user['_id'], update_fields)

            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('user_routes.edit_profile'))

    except Exception as e:
        flash(f'Erro ao tentar atualizar o perfil: {str(e)}', 'error')
        return redirect(url_for('user_routes.edit_profile'))



############################# Ver e editar perfil #############################


@user_routes.route('/list_users', methods=['GET'])
def list_users():  # Adiciona o parâmetro current_user
    try:
        users = get_all_users()  # Obtém todos os usuários do banco
        return render_template('list_users.html', users=users)  # Renderiza a lista
    except Exception as e:
        flash(f'Erro ao carregar a lista de usuários: {str(e)}', 'error')
        return redirect(url_for('user_routes.dashboard'))

@user_routes.route('/list_points', methods=['GET'])
def list_points():  # Adiciona o parâmetro current_user
    try:
        points = get_all_points()  # Obtém todos os usuários do banco
        return render_template('list_points.html', points=points)  # Renderiza a lista
    except Exception as e:
        flash(f'Erro ao carregar a lista de points: {str(e)}', 'error')
        return redirect(url_for('user_routes.dashboard'))

@user_routes.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)  # Ajuste para um único usuário
        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('user_routes.list_users'))

        # Obter a lista de IDs de pontos do checklist do usuário
        checklist_ids = user.get('checklist', [])

        # Consultar os pontos correspondentes aos IDs
        points = []
        for point_id in checklist_ids:
            point = get_point_by_id(point_id)  # Função que busca o ponto pelo ID
            if point:
                points.append(point)

        # Retornar o template com os detalhes do usuário e a lista de pontos
        return render_template('user_detail.html', user=user, points=points)
    except Exception as e:
        flash(f'Erro ao carregar o usuário: {str(e)}', 'error')
        return redirect(url_for('user_routes.list_users'))


@user_routes.route('/perfil/<user_id>', methods=['GET'])
def perfil(user_id):
    try:
        user = get_user_by_id(user_id)  # Ajuste para um único usuário
        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('user_routes.list_users'))

        # Retornar o template com os detalhes do usuário
        return render_template('perfil.html', user=user)  # Alterar para um template apropriado
    except Exception as e:
        flash(f'Erro ao carregar o usuário: {str(e)}', 'error')
        return redirect(url_for('user_routes.list_users'))



@user_routes.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user( user_id):  # Adiciona current_user como primeiro parâmetro
    try:
# Utilizando função do CRUD para buscar o usuário
        user = get_user_by_id(user_id)
        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('user_routes.login'))

        if request.method == 'GET':
            return render_template('edit_user.html', user=user)

        elif request.method == 'POST':
            email = request.form['email']
            password = request.form.get('password', None)
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            setor = request.form['setor']
            nivel = request.form['nivel']

            if email != user['email']:
                existing_user = get_user_by_email(email)
                if existing_user and existing_user['_id'] != user['_id']:
                    flash('Este e-mail já está cadastrado.', 'error')
                    return redirect(url_for('user_routes.edit_user', user=user))

            update_fields = {
                "email": email,
                "setor": setor,
                "nivel": nivel,
                "profile.first_name": first_name,
                "profile.last_name": last_name
            }

            if password:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                update_fields['password_hash'] = password_hash.decode('utf-8')

            update_user(user['_id'], update_fields)

            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('user_routes.list_users'))
    except Exception as e:
        flash(f'Erro ao tentar atualizar o perfil: {str(e)}', 'error')
        return redirect(url_for('user_routes.list_users'))

#atualiza o perfill do usuario com dados por urls
#necessario passar o id do usuario e o id do ponto
#se o ponto ja estiver no checklist, nao adiciona novamente
#atualiza as preferencias do usuario +1 sem limites
@user_routes.route('/update_user_qr/<user_id>/<point_id>', methods=['GET'])
def update_user_qr(user_id, point_id):
    try:
        user = get_user_by_id(user_id)
        point = get_point_by_id(point_id)

        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('user_routes.login'))

        if not point:
            flash('Ponto não encontrado.', 'error')
            return redirect(url_for('user_routes.login'))

        password = request.args.get('password', None)
        first_name = request.args.get('first_name')
        nascimento = request.args.get('nascimento')
        celular = request.args.get('celular')
        bairro = request.args.get('bairro')
        cidade = request.args.get('cidade')

        preferencias = user.get('preferencias', {
            "cultural": 0,
            "gastronomico": 0,
            "negocios": 0,
            "compras": 0,
            "aventura": 0,
            "religioso": 0,
            "eventos": 0,
            "historico": 0
        })

        categoria = point.get('categoria')
        if categoria in preferencias:
            preferencias[categoria] += 1
            print(f"Preferências atualizadas: {preferencias}")

        checklist_atual = user.get('checklist', [])

        if point_id not in checklist_atual:
            checklist_atual.append(point_id)

        # Mantendo o valor de selos inalterado
        selos_atual = user.get('selos', 0)

        # Atualizando os campos, mas sem alterar o valor de selos
        update_fields = {
            "first_name": first_name if first_name else user.get('first_name'),
            "data_nascimento": nascimento if nascimento else user.get('data_nascimento'),
            "celular": celular if celular else user.get('celular'),
            "bairro": bairro if bairro else user.get('bairro'),
            "cidade": cidade if cidade else user.get('cidade'),
            "selos": selos_atual,  # Manter o valor atual de selos
            "checklist": checklist_atual,
            "preferencias": preferencias
        }

        if password:
            update_fields["password_hash"] = password

        print(f"Campos atualizados: {update_fields}")
        update_user(user['_id'], update_fields)

        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('user_routes.get_user', user_id=user_id))

    except Exception as e:
        flash(f'Erro ao tentar atualizar o perfil: {str(e)}', 'error')
        return redirect(url_for('user_routes.dashboard'))

    

############################# Navegação entre páginas #############################


@user_routes.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",)

@user_routes.route("/selos")
def selos():
    return render_template("selos.html",)

@user_routes.route("/sucesso")
def sucesso():
    return render_template("sucesso.html",)

@user_routes.route("/desafios")
def desafios():
    return render_template("desafios.html",)

@user_routes.route("/login")
def login():
    return render_template("login.html",)

@user_routes.route("/link_create_user")
def link_create_user():
    return render_template("create_user.html",)

