import os
import sys
import logging
import requests
import psutil
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("execucao.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
LIMITE_DISCO_PERCENT = 80.0
LIMITE_RAM_PERCENT = 85.0
LIMITE_CPU_PERCENT = 90.0

def verificar_sistema():
    # Coleta de métricas nativas do sistema onde o script está rodando (Linux / Container)
    caminho_disco = "/"
    logging.info(f"Checando integridade do disco ({caminho_disco})...")
    
    uso_disco = psutil.disk_usage(caminho_disco).percent
    uso_ram = psutil.virtual_memory().percent
    uso_cpu = psutil.cpu_percent(interval=1)

    logging.info(f"Uso do disco ({caminho_disco}): {uso_disco}% | RAM: {uso_ram}% | CPU: {uso_cpu}%")

    alerta_disco = uso_disco >= LIMITE_DISCO_PERCENT
    alerta_ram = uso_ram >= LIMITE_RAM_PERCENT
    alerta_cpu = uso_cpu >= LIMITE_CPU_PERCENT

    status_critico = alerta_disco or alerta_ram or alerta_cpu

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
        logging.error("WEBHOOK_URL não encontrada no ambiente!")
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
        logging.info("Notificação enviada para o Teams com sucesso!")
    except Exception as e:
        logging.error(f"Falha ao enviar notificação para o Teams: {e}")

if __name__ == "__main__":
    verificar_sistema()
