import os
import logging
import psutil
import requests
from dotenv import load_dotenv

# Configura o sistema de logging acumulativo
logging.basicConfig(
    filename='execucao.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
LIMITE_DISCO_PERCENTUAL = 80.0

def enviar_alerta_teams(mensagem):
    if not WEBHOOK_URL:
        erro_msg = "Variavel WEBHOOK_URL nao encontrada no .env!"
        print(f"[ERRO] {erro_msg}")
        logging.error(erro_msg)
        return

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "📊 Relatório de Infraestrutura - Disco",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": mensagem,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code in [200, 202]:
            sucesso_msg = "Notificacao enviada para o Teams com sucesso!"
            print(f"[INFO] {sucesso_msg}")
            logging.info(sucesso_msg)
        else:
            recusa_msg = f"Teams recusou o envio. Codigo HTTP: {response.status_code}"
            print(f"[ERRO] {recusa_msg}")
            logging.error(recusa_msg)
    except Exception as e:
        falha_msg = f"Falha de conexao com o Webhook: {e}"
        print(f"[ERRO] {falha_msg}")
        logging.error(falha_msg)

def verificar_disco():
    # Prioridade de verificação do disco:
    # 1. Se existe a pasta mapeada do container (/host_disk) -> usa ela
    # 2. Se for Windows local -> usa 'C:\'
    # 3. Caso contrário -> usa a raiz Linux '/'
    if os.path.exists('/host_disk'):
        caminho_disco = '/host_disk'
    elif os.name == 'nt':
        caminho_disco = 'C:\\'
    else:
        caminho_disco = '/'

    uso_disco = psutil.disk_usage(caminho_disco)
    percentual_usado = uso_disco.percent

    msg_inicio = f"Checando integridade do disco ({caminho_disco})..."
    print(f"[INFO] {msg_inicio}")
    logging.info(msg_inicio)

    if percentual_usado >= LIMITE_DISCO_PERCENTUAL:
        alerta = f"ALERTA CRITICO: O disco ({caminho_disco}) atingiu {percentual_usado}% de capacidade!"
        print(f"[ALERTA] {alerta}")
        logging.warning(alerta)
        enviar_alerta_teams(alerta)
    else:
        status = f"Uso do disco ({caminho_disco}) em {percentual_usado}%. Operacao dentro da normalidade."
        print(f"[INFO] {status}")
        logging.info(status)
        enviar_alerta_teams(status)

if __name__ == "__main__":
    verificar_disco()
