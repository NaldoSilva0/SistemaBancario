# 🏦 Sistema Bancário - Python

Este é um sistema bancário robusto desenvolvido em Python, focado em **segurança de dados**, **persistência resiliente** e **lógica de negócios em tempo real**. O projeto simula as operações críticas de uma instituição financeira, desde o cadastro blindado de usuários até o rendimento automatizado de poupança.

---

## 🚀 Diferenciais do Projeto

O que torna este sistema especial não é apenas o que ele faz, mas **como** ele faz:

*   **Segurança Criptográfica:** Nenhuma senha é salva em texto puro. Utilizo o algoritmo `SHA-256` via biblioteca `hashlib` para garantir a total privacidade e segurança dos dados.
*   **Rendimento em Tempo Real:** A poupança utiliza lógica temporal (`datetime`) para calcular juros compostos baseados no tempo real decorrido (segundos/minutos) entre as sessões.
*   **Validação Rigorosa (Regex):** Implementação de expressões regulares para garantir políticas de senhas fortes (Obrigatório: Maiúsculas, minúsculas, números e caracteres especiais).
*   **Persistência de Dados:** Gerenciamento completo de estado via arquivos JSON com tratamento de exceções (`try/except`) para garantir que o sistema nunca quebre por falta de arquivos.
*   **Auditoria (Logs):** Cada movimentação financeira gera um log detalhado com carimbo de data/hora (Timestamp), criando um histórico imutável para o usuário.

---

## 🛠️ Funcionalidades

- [x] **Cadastro de Usuários:** Validação de nome (apenas letras), CPF único (bloqueio de duplicidade) e data de nascimento real.
- [x] **Sistema de Login:** Autenticação segura via comparação de hashes.
- [x] **Transferências Flexíveis:** Movimentações entre contas via ID ou CPF com validação de saldo.
- [x] **Poupança Inteligente:** Sistema de depósitos com rendimento automático calculado em background.
- [x] **Extrato e Auditoria:** Visualização de todo o histórico de logs da conta em tempo real.

---

## 💻 Tecnologias Utilizadas

*   **Linguagem:** Python 3.x
*   **Persistência:** JSON (JavaScript Object Notation)
*   **Principais Módulos:**
    *   `hashlib`: Proteção de credenciais com criptografia de via única.
    *   `re`: Validações complexas de padrões de texto.
    *   `datetime`: Controle de tempo, juros e logs.
    *   `json` & `os`: Gerenciamento e persistência no sistema de arquivos.

---

## 🏗️ Estrutura do Código (Arquitetura)

O projeto utiliza Programação Orientada a Objetos (POO) para organizar as responsabilidades:

*   **`main.py`**: Interface de linha de comando (CLI) e fluxo de interação.
*   **`persistencia.py`**: O "cérebro" do sistema. Gerencia o banco de dados JSON e a lógica de negócios.
*   **`usuario.py`**: Define a classe `Usuario`, responsável por estruturar os dados pessoais (Nome, CPF, Data de Nascimento).
*   **`conta.py`**: Define a classe `Conta`, que gerencia o saldo, ID, poupança e logs, além de possuir o método `to_dict()` para conversão de dados.

---

## 🔧 Como Executar

1. Clone o repositório:
   ```bash
   git clone [https://github.com/NaldoSilva0/SistemaBancario.git](https://github.com/NaldoSilva0/SistemaBancario.git)
   ```

2. Navegue até a pasta do projeto:
   ```bash
   cd SistemaBancario
   ```

3. Execute a aplicação:
   ```bash
   python main.py
   ```

---

⭐ **Desenvolvido por [Naldo Silva](https://github.com/NaldoSilva0)**
*Estudante de desenvolvimento focado em construir soluções seguras e eficientes.*
