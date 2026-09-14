import os
import sys
import json
import logging
import requests
import psutil
from dotenv import load_dotenv

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

handler_file = logging.FileHandler("execucao.log", encoding="utf-8")
handler_stdout = logging.StreamHandler(sys.stdout)

formatter = JsonFormatter()
handler_file.setFormatter(formatter)
handler_stdout.setFormatter(formatter)

logger.addHandler(handler_file)
logger.addHandler(handler_stdout)

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
LIMITE_DISCO_PERCENT = 80.0
LIMITE_RAM_PERCENT = 85.0
LIMITE_CPU_PERCENT = 90.0

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

    # Log estruturado com as métricas do sistema
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
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Notificação enviada para o Teams com sucesso.")
    except Exception as e:
        logger.error(f"Falha ao enviar notificação para o Teams: {e}")

if __name__ == "__main__":
    verificar_sistema()
