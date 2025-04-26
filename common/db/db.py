from common.settings.settings import settings
from utils.log import setup_logging
from sqlalchemy import create_engine, text
from time import sleep
from typing import Optional, Dict, Any

MAX_ATTEMPTS = 4
log = setup_logging(log_file="logs/banco.log")

class Banco:
    @staticmethod
    def conexao(base: str) -> Optional[Any]:
        """Estabelece a conexão com o banco de dados."""
        log.info(f"Iniciando tentativa de conexão | Base: {base}")
        urls: Dict[str, str] = {
            'local': settings.BASE
        }
        
        if base not in urls:
            log.error(f"Base '{base}' não encontrada nas configurações. Informe a equipe de desenvolvimento.")
            return None
        
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                engine = create_engine(urls[base])
                conexao = engine.connect()
                log.info(f"Conexão estabelecida com sucesso | Base: {base} | Tentativa: {attempt}")
                return conexao
            except Exception as e:
                log.warning(f"Erro de conexão | Base: {base} | Tentativa: {attempt}/{MAX_ATTEMPTS} | Erro: {e}", exc_info=True)
                sleep(2 ** attempt)  # Exponential backoff

        log.error(f"Falha definitiva: não foi possível conectar à base '{base}' após {MAX_ATTEMPTS} tentativas.")
        return None
    
    @staticmethod
    def consulta(params: Dict[str, Any], sql: str, base: str) -> Optional[Any]:
        """Executa uma consulta SQL e retorna o resultado."""
        log.info(f"Iniciando consulta no banco | Base: {base} | Parâmetros: {params}")
        session = None
        
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                session = Banco.conexao(base)
                if not session:
                    log.error(f"Não foi possível estabelecer conexão para consulta | Base: {base}")
                    return None

                resultado = session.execute(text(sql), params).fetchall()
                
                if not resultado:
                    log.warning(f"Consulta sem resultados | Base: {base} | Parâmetros: {params}")
                    return None

                log.info(f"Consulta realizada com sucesso | Base: {base} | Linhas retornadas: {len(resultado)}")
                return resultado

            except Exception as e:
                log.warning(f"Erro ao executar consulta | Tentativa: {attempt}/{MAX_ATTEMPTS} | SQL: {sql} | Erro: {e}", exc_info=True)
                sleep(2 ** attempt)

            finally:
                if session:
                    session.close()
                    log.debug(f"Conexão encerrada após tentativa de consulta | Base: {base}")

        log.error(f"Falha definitiva: consulta não realizada após {MAX_ATTEMPTS} tentativas | Base: {base}")
        return None
    
    @staticmethod
    def executa(params: Dict[str, Any], sql: str, base: str) -> bool:
        """Executa comandos INSERT, UPDATE ou DELETE no banco de dados."""
        log.info(f"Iniciando execução de comando no banco | Base: {base} | Parâmetros: {params}")
        session = None

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                session = Banco.conexao(base)
                if not session:
                    log.error(f"Não foi possível estabelecer conexão para execução de comando | Base: {base}")
                    return False

                session.execute(text(sql), params)
                session.commit()
                log.info(f"Comando executado e transação confirmada com sucesso | Base: {base}")
                return True

            except Exception as e:
                log.warning(f"Erro ao executar comando no banco | Tentativa: {attempt}/{MAX_ATTEMPTS} | SQL: {sql} | Erro: {e}", exc_info=True)
                sleep(2 ** attempt)

            finally:
                if session:
                    session.close()
                    log.debug(f"Conexão encerrada após tentativa de execução | Base: {base}")

        log.error(f"Falha definitiva: comando não executado após {MAX_ATTEMPTS} tentativas | Base: {base}")
        return False

db = Banco()
