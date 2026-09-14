# Sistema de Monitoramento de Infraestrutura & Observabilidade

Este projeto é um agente automatizado desenvolvido em Python para monitorar recursos do sistema (Disco, Memória RAM e CPU) dentro de ambientes Linux/Containers, enviando alertas em tempo real via Webhook para o Microsoft Teams.

## 🚀 Funcionalidades

- **Coleta Multi-Métrica:** Monitoramento contínuo de Uso de Disco (`/`), Memória RAM e Uso de CPU.
- **Observabilidade Profissional:** Logs estruturados em formato **JSON** com timestamps e metadados detalhados para indexação e análise.
- **Resiliência Integrada:** Política de retentativa automática (*Retry logic* com *Exponential Backoff*) no envio de Webhooks.
- **Integração CI/CD:** Esteira automatizada via **GitHub Actions** validando compilação Python, sintaxe e build da imagem Docker a cada push.
- **Alertas Dinâmicos:** Cartões adaptativos no Microsoft Teams diferenciando relatórios de rotina (🟢) e alertas críticos (🔴).

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
