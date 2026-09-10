import datetime
import psutil
import requests

# Limite percentual de uso de disco
LIMITE_DISCO_PERCENTUAL = 80.0

# COLE A SUA URL DO WEBHOOK DO TEAMS ENTRE AS ASPAS ABAIXO:
WEBHOOK_URL = "https://defaultfbcbd4a1cffc4c50b5a8611abdfe17.8c.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/30/workflows/4b8cfa9661eb45d997e36155975e3dee/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ubSgsAytkgQGnthj58kyYtKxfHAiEWZOFXBPxvLejAM"

def enviar_alerta_teams(mensagem, status_critico=False):
    if WEBHOOK_URL == "SUA_URL_DO_WEBHOOK_AQUI":
        print("[AVISO] Cole a URL do Webhook na variável WEBHOOK_URL para enviar para o Teams.")
        return

    cor_header = "Attention" if status_critico else "Good"
    
    # Formato do payload para o Microsoft Teams
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "🚨 Monitoramento de Infraestrutura N2" if status_critico else "📊 Status de Rotina - TI",
                            "weight": "Bolder",
                            "size": "Medium",
                            "color": cor_header
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
        response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code in [200, 202]:
            print("[INFO] Alerta enviado para o Teams com sucesso!")
        else:
            print(f"[ERRO] Falha ao enviar para o Teams. Código HTTP: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro de conexão com o Webhook: {e}")

def verificar_disco():
    uso_disco = psutil.disk_usage('C:\\')
    percentual_usado = uso_disco.percent
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{data_hora}] Checando integridade do disco C:...")
    
    if percentual_usado >= LIMITE_DISCO_PERCENTUAL:
        alerta = f"**ALERTA CRÍTICO**: O disco C: do servidor/máquina atingiu **{percentual_usado}%** de capacidade!"
        print(f"[{data_hora}] {alerta}")
        enviar_alerta_teams(alerta, status_critico=True)
    else:
        status = f"Uso do disco C: em **{percentual_usado}%**. Operação dentro da normalidade."
        print(f"[{data_hora}] {status}")
        enviar_alerta_teams(status, status_critico=False)

if __name__ == "__main__":
    verificar_disco()
