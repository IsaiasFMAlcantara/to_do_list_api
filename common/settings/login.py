import re
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from utils.log import setup_logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
log = setup_logging(log_file='logs/login.log')

class LoginClass:
    def _validar_email(self, email):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(padrao, email))
        
        if is_valid:
            log.info(f"E-mail validado com sucesso: {email}")
        else:
            log.warning(f"E-mail inválido informado: {email}")
        
        return {
            'retorno': 'E-mail válido' if is_valid else 'E-mail inválido',
            'status': is_valid
        }

    def _validar_senha(self, senha, hash_senha):
        try:
            is_valid = pwd_context.verify(senha, hash_senha)
            log.info("Validação de senha concluída.") if is_valid else log.warning("Senha inválida na validação.")
            return is_valid
        except (UnknownHashError, ValueError) as e:
            log.error(f"Erro ao validar senha: {str(e)}", exc_info=True)
            return False

    def _criar_hash(self, senha):
        try:
            log.info("Iniciando criação de hash da senha.")
            return pwd_context.hash(senha)
        except Exception as e:
            log.error(f"Erro crítico ao criar hash da senha: {str(e)}", exc_info=True)
            raise Exception(f"Erro ao criar hash da senha: {str(e)}")

    def criar_conta(self, nome, senha, email):
        log.info(f"Iniciando criação de conta para: {nome} ({email})")
        email_validacao = self._validar_email(email)
        
        if not email_validacao['status']:
            log.warning(f"Conta não criada: E-mail inválido para {nome}")
            return {'retorno': 'E-mail inválido.', 'status': False}

        try:
            hash_senha = self._criar_hash(senha)
            log.info(f"Conta criada com sucesso para: {nome}")
            return {
                "name": nome,
                "password": hash_senha,
                "v_email": email
            }
        except Exception as e:
            log.error(f"Erro ao criar conta para {nome}: {str(e)}", exc_info=True)
            return {'retorno': str(e), 'status': False}

    def login(self, senha_digitada, hash_senha_armazenado):
        if not senha_digitada or not hash_senha_armazenado:
            log.warning('Tentativa de login com senha ou hash não fornecido.')
            return {
                'retorno': 'Senha ou hash não fornecido.',
                'status': False
            }

        if self._validar_senha(senha_digitada, hash_senha_armazenado):
            log.info("Login realizado com sucesso.")
            return {
                'retorno': 'Login realizado com sucesso.',
                'status': True
            }
        else:
            log.warning('Tentativa de login falhou: senha incorreta.')
            return {
                'retorno': 'Senha incorreta.',
                'status': False
            }

    def trocar_senha(self, senha_atual, hash_senha_atual, iduser, email, nova_senha):
        log.info(f"Solicitação de troca de senha recebida para usuário ID {iduser} - {email}")

        if not self._validar_senha(senha_atual, hash_senha_atual):
            log.warning(f"Troca de senha negada: senha atual incorreta para usuário ID {iduser}")
            return {
                'retorno': "Senha atual incorreta. Não é possível trocar a senha.",
                'status': False
            }
        
        try:
            novo_hash = self._criar_hash(nova_senha)
            log.info(f"Senha trocada com sucesso para usuário ID {iduser}")
            return {
                'iduser': iduser,
                'email': email,
                'senha': novo_hash
            }
        except Exception as e:
            log.error(f"Erro crítico na troca de senha para usuário ID {iduser}: {str(e)}", exc_info=True)
            return {'retorno': str(e), 'status': False}
    
    def atualizar_informacoes(self, iduser: int, nome: str, email: str) -> dict:
        log.info(f"Atualizando informações do usuário | ID: {iduser} | Nome: {nome} | Email: {email}")

        # Validação rápida (opcional, mas profissional)
        if not all([iduser, nome, email]):
            log.error(f"Dados inválidos para atualização: iduser={iduser}, nome={nome}, email={email}")
            return {'status': False, 'erro': 'Dados incompletos para atualização.'}

        return {
            'p_id': iduser,
            'p_username': nome.strip(),
            'p_email': email.strip()
        }

# Instanciando a classe
fusers = LoginClass()
