1.1. Criar e abrir o arquivo README.md:
Comando: notepad.
No terminal, dentro da pasta do seu projeto, execute:
Bash
notepad README.md
O que esse comando faz: Se o arquivo não existir, o Windows vai perguntar se deseja criá-lo (clique em Sim). 
O Bloco de Notas será aberto em seguida.

2.2. Colar o conteúdo formatado:

Interface Gráfica.Copie todo o texto no bloco abaixo e cole dentro da janela do Bloco de Notas:

Plaintext# 

📊 Automação de Monitoramento de Infraestrutura N2

Projeto de automação desenvolvido em Python para monitoramento de saúde do sistema (uso de disco C:) e disparo de alertas em tempo real para o Microsoft Teams via Webhooks seguros.

---

## 🚀 Tecnologias e Ferramentas

* **Linguagem:** Python 3.x
* **Bibliotecas:** `psutil` (métricas de sistema), `requests` (integração HTTP API), `python-dotenv` (variáveis de ambiente)
* **Comunicação:** Microsoft Teams (Workflows / Webhook de entrada)
* **Controle de Versão:** Git & GitHub

---

## 🛠️ Arquitetura e Segurança (DevSecOps)

* **Variáveis de Ambiente:** A URL sensível do Webhook é armazenada em um arquivo `.env` local.
* **Git Hygiene:** O arquivo `.gitignore` foi configurado para proibir o versionamento do `.env`, protegendo credenciais sensíveis contra vazamentos no GitHub.

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos
* Python 3 instalado
* Git Bash ou terminal Linux

### Passo a Passo

1. **Clone o repositório:**
bashgit clone https://github.com/SEU_USUARIO/automacao-suporte.gitcd automacao-suporte
2. **Instale as dependências:**
bashpip install psutil requests python-dotenv
3. **Configure as Variáveis de Ambiente:**
Crie um arquivo `.env` na raiz do projeto com a URL do Teams:
textWEBHOOK_URL=https://sua-url-do-webhook-aqui
4. **Execute o Script:**
bashpython check_sistema.py
3.3. Salvar e fechar:Atalho: Ctrl + S.Pressione Ctrl + S no teclado para salvar e feche a janela do Bloco de Notas.