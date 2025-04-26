from common.settings.settings import settings
from utils.log import setup_logging
from sqlalchemy import create_engine, text
from time import sleep
from typing import Optional, Dict, Any

MAX_ATTEMPTS = 4
log = setup_logging(log_file="banco.log")

class Banco:
    @staticmethod
    def conexao(base: str) -> Optional[Any]:
        """Estabelece a conexão com o banco de dados."""
        urls: Dict[str, str] = {
            'local': settings.BASE
        }
        
        if base not in urls:
            log.error(f"Base '{base}' informada não encontrada. Favor informar equipe de desenvolvimento.")
            return None
        
        for attempt in range(MAX_ATTEMPTS):
            try:
                engine = create_engine(urls[base])
                conexao = engine.connect()
                log.info(f"Conexão estabelecida com sucesso | Base: {base}")
                return conexao
            except Exception as e:
                log.warning(f"Erro de conexão | Base: {base} | Tentativa: {attempt + 1} de {MAX_ATTEMPTS} | Erro: {e}")
                sleep(2 ** attempt)  # Exponencial backoff para novas tentativas

        log.error(f"Falha na conexão após {MAX_ATTEMPTS} tentativas | Base: {base}")
        return None
    
    @staticmethod
    def consulta(params: Dict[str, Any], sql: str, base: str) -> Optional[Any]:
        """Executa uma consulta SQL e retorna o resultado."""
        session = None
        
        for attempt in range(MAX_ATTEMPTS):
            try:
                session = Banco.conexao(base)
                if not session:
                    return None  # Retorna None se a conexão falhou.

                resultado = session.execute(text(sql), params).fetchall()
                
                if not resultado:
                    log.warning(f"Consulta sem resultados | Parâmetro: {params} | Base: {base}")
                    return None

                log.info(f"Consulta executada com sucesso | Base: {base}")
                return resultado

            except Exception as e:
                log.warning(f"Erro na consulta | Tentativa: {attempt + 1} de {MAX_ATTEMPTS} | Erro: {e}")
                sleep(2 ** attempt)  # Exponencial backoff

            finally:
                if session:
                    session.close()

        log.error(f"Falha na execução da consulta após {MAX_ATTEMPTS} tentativas | Base: {base}")
        return None
    
    @staticmethod
    def executa(params: Dict[str, Any], sql: str, base: str) -> bool:
        """Executa comandos INSERT, UPDATE ou DELETE no banco de dados."""
        session = None

        for attempt in range(MAX_ATTEMPTS):
            try:
                session = Banco.conexao(base)
                if not session:
                    return False  # Falhou a conexão

                session.execute(text(sql), params)
                session.commit()
                log.info(f"Comando executado com sucesso | Base: {base}")
                return True

            except Exception as e:
                log.warning(f"Erro ao executar comando | Tentativa: {attempt + 1} de {MAX_ATTEMPTS} | Erro: {e}")
                sleep(2 ** attempt)

            finally:
                if session:
                    session.close()

        log.error(f"Falha ao executar comando após {MAX_ATTEMPTS} tentativas | Base: {base}")
        return False


db = Banco()