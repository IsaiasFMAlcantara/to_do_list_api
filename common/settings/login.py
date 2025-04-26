import re
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginClass:
    def _validar_email(self, email):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return {
            'retorno': 'E-mail válido' if re.match(padrao, email) else 'E-mail inválido',
            'status': bool(re.match(padrao, email))
        }

    def _validar_senha(self, senha, hash_senha):
        try:
            return pwd_context.verify(senha, hash_senha)
        except (UnknownHashError, ValueError):
            return False

    def _criar_hash(self, senha):
        try:
            return pwd_context.hash(senha)
        except Exception as e:
            raise Exception(f"Erro ao criar hash da senha: {str(e)}")

    def criar_conta(self, nome, senha, email):
        if self._validar_email(email):
            try:
                hash_senha = self._criar_hash(senha)
                return {
                    "name": nome,
                    "password": hash_senha,
                    "v_email":email
                }
            except Exception as e:
                return {'retorno': str(e), 'status': False}

    def login(self, senha_digitada, hash_senha_armazenado):
        """
        Faz login comparando a senha digitada com o hash salvo.
        Retorna dicionário padronizado: sucesso ou erro.
        """
        if not senha_digitada or not hash_senha_armazenado:
            return {
                'retorno': 'Senha ou hash não fornecido.',
                'status': False
            }

        if self._validar_senha(senha_digitada, hash_senha_armazenado):
            return {
                'retorno': 'Login realizado com sucesso.',
                'status': True
            }
        else:
            return {
                'retorno': 'Senha incorreta.',
                'status': False
            }

    def trocar_senha(self, senha_atual, hash_senha_atual, iduser, email, nova_senha):
        if not self._validar_senha(senha_atual, hash_senha_atual):
            return {
                'retorno': "Senha atual incorreta. Não é possível trocar a senha.",
                'status': False
            }
        
        try:
            novo_hash = self._criar_hash(nova_senha)
            return {
                'iduser': iduser,
                'email': email,
                'senha': novo_hash,
                'status': True
            }
        except Exception as e:
            return {'retorno': str(e), 'status': False}

# Instanciando a classe
fusers = LoginClass()
