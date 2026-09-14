import os
import sys
import json
import logging
import requests
import psutil
from datetime import datetime
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Formatador customizado para logs em JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_object = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        if hasattr(record, "extra_data"):
            log_object["data"] = record.extra_data
        return json.dumps(log_object, ensure_ascii=False)

# Configuração do Logger
logger = logging.getLogger("MonitorSistema")
logger.setLevel(logging.INFO)

# Configura o arquivo de log com o nome contendo a data atual (ex: execucao_2026-09-14.log)
data_hoje = datetime.now().strftime("%Y-%m-%d")
nome_arquivo_log = f"execucao_{data_hoje}.log"

# Handler de arquivo com rotação diária (mantém histórico dos últimos 30 dias)
handler_file = TimedRotatingFileHandler(
    filename=nome_arquivo_log,
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)
handler_stdout = logging.StreamHandler(sys.stdout)

formatter = JsonFormatter()
handler_file.setFormatter(formatter)
handler_stdout.setFormatter(formatter)

logger.addHandler(handler_file)
logger.addHandler(handler_stdout)

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Limites operacionais de produção
LIMITE_DISCO_PERCENT = 80.0
LIMITE_RAM_PERCENT = 85.0
LIMITE_CPU_PERCENT = 90.0

def criar_sessao_com_retry():
    session = requests.Session()
    estrategia_retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=estrategia_retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def verificar_sistema():
    caminho_disco = "/"
    logger.info("Iniciando checagem de integridade do sistema.")
    
    uso_disco = psutil.disk_usage(caminho_disco).percent
    uso_ram = psutil.virtual_memory().percent
    uso_cpu = psutil.cpu_percent(interval=1)

    alerta_disco = uso_disco >= LIMITE_DISCO_PERCENT
    alerta_ram = uso_ram >= LIMITE_RAM_PERCENT
    alerta_cpu = uso_cpu >= LIMITE_CPU_PERCENT

    status_critico = alerta_disco or alerta_ram or alerta_cpu

    metricas = {
        "disco_caminho": caminho_disco,
        "disco_uso_percent": uso_disco,
        "ram_uso_percent": uso_ram,
        "cpu_uso_percent": uso_cpu,
        "status_critico": status_critico
    }
    logger.info("Metricas coletadas com sucesso.", extra={"extra_data": metricas})

    titulo = "⚠️ ALERTA DE RECURSOS DO SISTEMA" if status_critico else "✅ Relatório de Integridade do Sistema"
    
    mensagem = (
        f"**Status do Container/VM Linux:**\n\n"
        f"- **Disco ({caminho_disco}):** {uso_disco}% {'🔴 (Limite Atingido)' if alerta_disco else '🟢'}\n"
        f"- **Memória RAM:** {uso_ram}% {'🔴 (Limite Atingido)' if alerta_ram else '🟢'}\n"
        f"- **Uso de CPU:** {uso_cpu}% {'🔴 (Limite Atingido)' if alerta_cpu else '🟢'}"
    )

    enviar_notificacao_teams(titulo, mensagem)

def enviar_notificacao_teams(titulo, mensagem):
    if not WEBHOOK_URL:
        logger.warning("WEBHOOK_URL não encontrada no ambiente! Notificação não enviada.")
        return

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptivecard.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {"type": "TextBlock", "text": titulo, "weight": "Bolder", "size": "Medium"},
                        {"type": "TextBlock", "text": mensagem, "wrap": True}
                    ]
                }
            }
        ]
    }

    try:
        session = criar_sessao_com_retry()
        response = session.post(WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Notificação enviada para o Teams com sucesso.")
    except Exception as e:
        logger.error(f"Falha ao enviar notificação para o Teams após retentativas: {e}")

if __name__ == "__main__":
    verificar_sistema()
