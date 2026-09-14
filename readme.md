# Sistema de Monitoramento de Infraestrutura & Observabilidade

Este projeto é um agente automatizado desenvolvido em Python para monitorar recursos do sistema (Disco, Memória RAM e CPU) dentro de ambientes Linux/Containers, enviando alertas em tempo real via Webhook para o Microsoft Teams.

## 🚀 Funcionalidades

- **Coleta Multi-Métrica:** Monitoramento contínuo de Uso de Disco (`/`), Memória RAM e CPU.
- **Logs Estruturados em JSON:** Registro de execuções no formato JSON.
- **Rotação Diária de Logs:** Os logs são salvos em arquivos individuais por data (`execucao_YYYY-MM-DD.log`).
- **Resiliência Integrada:** Retentativa automática em caso de falhas de rede no envio do Webhook.
- **Alertas Dinâmicos:** Mensagens diferenciadas para relatórios normais (🟢) e alertas críticos (🔴).

## 🧰 Stack Tecnológica

- **Python 3.11** (`psutil`, `requests`, `python-dotenv`)
- **Docker & Docker Compose**
- **GitHub Actions (CI/CD)**
- **Microsoft Teams Webhook (Adaptive Cards)**

## 📦 Como Executar

### 1. Configuração do Ambiente
Crie um arquivo `.env` na raiz do projeto com a URL do seu Webhook:

env
WEBHOOK_URL=https://sua-url-webhook.teams.microsoft.com/...


### 2. Execução via Docker Compose
bash
docker compose up --build


---
*Projeto em evolução - Parte 3 Concluído.*
