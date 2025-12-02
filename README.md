# API Hoteis - AV2 Claudiane 🏖️

![Version](https://img.shields.io/badge/version-0.1.5-blue)
![OAS](https://img.shields.io/badge/OAS-3.1-orange)
![License](https://img.shields.io/badge/license-Apache_2.0-green)

## 🏨 Sistema de Gestão de Reservas de Hoteis

Esta API permite gerenciar todo o ciclo de vida de uma reserva de hotel, garantindo integridade e eficiência nos processos.

### ✨ Funcionalidades Principais

* **Hotéis:** Cadastro completo, busca de hotéis e gerenciamento de quartos (acomodações).
* **Clientes:** Gestão de hóspedes, histórico e dados pessoais.
* **Reservas:** Criação de reservas, verificação automática de disponibilidade e controle de datas (check-in/out).
* **Pagamentos:** Registro e validação de transações financeiras associadas às reservas.

---

### ▶️ Iniciar Servidor.

Para iniciar a api, você precisa:

* **Instalar os Requeriments:** ```pip install -r requeriments.txt```
* **Configurar o DB a Ser Utilizado:** Ir na pasta do projeto, **app/databases/**, e renomear um dos dois arquivos existentes [database.py.oracle ou database.py.sqlite] para **database.py**.
* **Iniciar o Servidor:** ``` python -m uvicorn main:app ```

Nota: As credenciais do database presente no arquivo *login_live_oracle.json*, precisam ser inseridas ao utilizar DB Oracle Live.
Nota 2: A pasta [instantclient](https://www.oracle.com/database/technologies/instant-client/downloads.html) é usada exclusivamente para a conexão com DB Oracle (Thick Mode). Para conexão deve extrair o arquivo *instantclient*.
Nota 3: O arquivo *hotel.db* presente na pasta *app/databases/* é um DB de exemplo para uso da solução com SQLite. Para inicio limpo, basta exclui-lo.


---

### 📚 Links Úteis

* **Especificação OpenAPI (JSON):** [`/openapi.json`](/openapi.json)
* **Repositório do Código:** [Link diretório GitHub](https://github.com/andreluiz05/sistema_busca_hotel)
---

### 💚 Criadores
* Enio Enrique: [Link Perfil GitHub](https://github.com/dryeniio)
* André Luiz: [Link Perfil GitHub](https://github.com/andreluiz05)

### 📜 Licença

Este projeto é distribuído sob a licença **Apache 2.0**.
