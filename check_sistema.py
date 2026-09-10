import datetime
import psutil

LIMITE_DISCO_PERCENTUAL = 80.0

def verificar_disco():
    uso_disco = psutil.disk_usage('C:\\')
    percentual_usado = uso_disco.percent
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{data_hora}] Verificando integridade do sistema...")
    print(f"Uso do Disco C: {percentual_usado}%")

    if percentual_usado >= LIMITE_DISCO_PERCENTUAL:
        alerta = f"[ALERTA CRÍTICO] Espaço em disco acima de {LIMITE_DISCO_PERCENTUAL}%!"
        gerar_log(data_hora, alerta)
        print(alerta)
    else:
        status = "[OK] Espaço em disco dentro do limite operacional."
        gerar_log(data_hora, status)
        print(status)

def gerar_log(data_hora, mensagem):
    with open("relatorio_suporte.log", "a", encoding="utf-8") as f:
        f.write(f"{data_hora} - {mensagem}\n")

if __name__ == "__main__":
    verificar_disco()
