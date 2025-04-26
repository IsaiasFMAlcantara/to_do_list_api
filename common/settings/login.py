import re
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginClass:
    def _validar_email(self, email):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(padrao, email):
            return {
                'retorno':'E-mail valido',
                'status':True
            }
        else:
            return {
                'retorno':'E-mail inválido.',
                'status':False
            }

    def _validar_senha(self, pw, hh):
        try:
            verify = pwd_context.verify(pw, hh)
            return verify
        except UnknownHashError:
            return False

    def _criar_hash(self, senha):
        try:
            return pwd_context.hash(senha)
        except Exception as e:
            return {
                'retorno':f"Erro ao criar o hash: {e}",
                'status':False
            }

    def criar_conta(self, nome, email, password, marcas=None, colunas=None):
        if self._validar_email(email):
            hash_senha = self._criar_hash(password)
            if hash_senha:
                informacoes = {
                    'nome': nome,
                    'senha': hash_senha,
                    'marcas': marcas or [],
                    'colunas': colunas or []
                }
                return informacoes
            else:
                return {
                    'retorno':"Erro ao criar conta. Não foi possível gerar o hash da senha.",
                    'status':False
                }
        else:
            return None

    def login(self, hash_password, password):
        validate = self._validar_senha(password, hash_password)
        return validate

    def trocar_senha(self, password, hash_password, iduser, email, new_password):
        if self._validar_senha(password, hash_password):
            nova_senha_hash = self._criar_hash(new_password)
            if nova_senha_hash:
                informacoes = {
                    'iduser': iduser,
                    'email': email,
                    'senha': nova_senha_hash,
                }
                return informacoes
            else:
                return {
                    'retorno':"Erro ao criar o hash para a nova senha.",
                    'status':False
                }
        else:
            return {
                'retorno':"Senha atual incorreta. Não é possível trocar a senha.",
                'status':False
            }


login_email = LoginClass()
