# API Hoteis - AV2 Claudiane 🏖️

![Version](https://img.shields.io/badge/version-0.1.4-blue)
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

* **Instalar os Requeriments:** ```pip install requeriments.txt```
* **Configurar o DB a Ser Utilizado:** Ir na pasta do projeto, **app/databases/**, e renomear um dos dois arquivos existentes [database.py.oracle ou database.py.sqlite] para **database.py**
* **Iniciar o Servidor:** ``` python -m uvicorn main:app ```


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
