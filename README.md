# Sistema de Gerenciamento de Pedidos

Desenvolvido em Python, executado via terminal e com persistência de dados em arquivos JSON.

Foco em organização de código, Programação Orientada a Objetos, separação de responsabilidades, tratamento de exceções, validação de dados e persistência segura.

Atualmente, esta versão utiliza arquivos JSON como armazenamento. Futuras versões poderão substituir a persistência em arquivos por banco de dados relacional.

---

## Sobre o projeto

O **Sistema de Gerenciamento de Pedidos** permite controlar produtos e pedidos por meio de uma interface de terminal.

O projeto foi desenvolvido como estudo e portfólio, com o objetivo de aplicar conceitos de Python em uma aplicação completa, separando responsabilidades entre domínio, serviços, repositórios e interface.

Entre os conceitos praticados estão:

- Programação Orientada a Objetos;
- encapsulamento;
- properties, getters e setters;
- composição entre classes;
- type hints;
- tratamento e propagação de exceções;
- separação de responsabilidades;
- camada de serviços;
- padrão Repository;
- persistência em JSON;
- validação de dados;
- funções genéricas com `Callable` e `TypeVar`;
- uso de `classmethod`;
- constantes e estados de domínio;
- proteção de coleções internas;
- manipulação segura de arquivos;
- organização modular do projeto.

---

## Funcionalidades

### Produtos

O sistema permite:

- cadastrar produtos;
- buscar produtos;
- listar produtos cadastrados;
- editar produtos;
- validar nome e preço;
- impedir dados inválidos;
- verificar existência de produtos;
- identificar repositório vazio.

Os produtos possuem validações de domínio para atributos como nome e preço.

### Pedidos

O sistema permite:

- criar novos pedidos;
- associar dados do cliente ao pedido;
- gerar número identificador para cada pedido;
- buscar pedidos pelo número;
- listar pedidos cadastrados;
- adicionar produtos ao pedido;
- remover produtos do pedido;
- controlar quantidade dos itens;
- calcular subtotal dos itens;
- calcular valor total do pedido;
- selecionar forma de pagamento;
- finalizar pedidos;
- cancelar pedidos;
- impedir operações inválidas em pedidos finalizados ou cancelados;
- exportar pedidos.

### Itens do pedido

Cada item do pedido contém informações relacionadas ao produto e à quantidade adicionada.

Nome e preço podem ser preservados como snapshots do momento em que o produto foi incluído no pedido, evitando que alterações posteriores no cadastro do produto modifiquem indevidamente informações históricas.

A coleção interna de itens também possui proteção contra alterações externas diretas.

### Formas de pagamento

O projeto possui suporte a diferentes formas de pagamento por meio de classes especializadas.

O sistema permite:

- listar formas de pagamento disponíveis;
- selecionar uma forma de pagamento;
- reconstruir a forma de pagamento a partir dos dados persistidos;
- impedir finalização de pedidos sem as condições necessárias.

---

## Persistência de dados

Atualmente os dados são armazenados em arquivos JSON localizados na pasta:


data/


A aplicação utiliza repositories para acessar e alterar os dados persistidos.

As demais camadas da aplicação não precisam manipular diretamente os arquivos JSON.

Fluxo geral:


Interface
    ↓
Service
    ↓
Repository
    ↓
JSON


Essa separação permite que futuramente a persistência JSON seja substituída por um banco de dados sem exigir a reescrita completa das regras de negócio e da interface.

---

## Gravação segura dos arquivos JSON

A aplicação utiliza arquivos temporários durante operações de gravação.

Em vez de sobrescrever diretamente o arquivo principal, os novos dados são inicialmente escritos em um arquivo temporário.

Fluxo simplificado:


dados atuais
    ↓
arquivo .temp
    ↓
gravação concluída
    ↓
substituição do JSON original


Caso uma falha aconteça durante a gravação, o arquivo principal não é imediatamente sobrescrito.

Na inicialização, o sistema também verifica a existência de arquivos temporários não tratados e alerta o usuário quando necessário.

---

## Tratamento de arquivos corrompidos

O sistema diferencia situações como:

- arquivo inexistente;
- repositório vazio;
- arquivo JSON corrompido.

Um arquivo JSON corrompido não é interpretado automaticamente como um repositório vazio.

Isso reduz o risco de dados existentes serem substituídos indevidamente por uma nova estrutura vazia.

A detecção ocorre na camada de persistência, enquanto a apresentação da mensagem de erro fica sob responsabilidade da interface.

---

## Arquitetura

O projeto busca separar cada responsabilidade em uma camada específica.

Estrutura principal:


sistema-gerenciamento-pedidos/
│
├── .gitignore
├── main.py
├── README.md
│
├── app/
│   ├── config/
│   ├── domain/
│   ├── interface/
│   ├── repositories/
│   ├── services/
│   └── utils/
│
└── data/


### `config`

Contém configurações e constantes utilizadas pela aplicação.

Centralizar essas informações reduz valores espalhados pelo código e facilita alterações futuras.

### `domain`

Contém as classes que representam as entidades e regras fundamentais do sistema.

Exemplos:

- produto;
- pedido;
- item de pedido;
- cliente;
- formas de pagamento.

As entidades são responsáveis por proteger seus próprios estados e manter suas regras de validade.

### `interface`

Responsável pela interação com o usuário através do terminal.

Inclui:

- menus;
- funções de entrada;
- mensagens de saída;
- tratamento visual de determinados erros;
- helpers específicos da interface.

A interface utiliza os services para executar as operações do sistema.

### `repositories`

Responsáveis pela persistência e recuperação dos dados.

Atualmente utilizam arquivos JSON.

Essa camada concentra operações como:

- leitura;
- busca;
- inclusão;
- substituição;
- persistência.

Futuramente os repositories poderão ser adaptados para utilizar um banco de dados.

### `services`

Contém os casos de uso e regras que coordenam operações entre diferentes objetos e repositories.

A camada de serviço não é responsável por:

- realizar `input()`;
- imprimir mensagens para o usuário;
- manipular diretamente arquivos JSON.

Isso reduz o acoplamento entre as regras da aplicação e a interface de terminal.

### `utils`

Contém funções utilitárias reutilizáveis que dão suporte a diferentes partes da aplicação.

Essa pasta concentra recursos auxiliares que não pertencem diretamente às regras de negócio, à interface ou aos repositories, como manipulação de arquivos JSON, conversões e verificações genéricas utilizadas por múltiplos módulos.

O objetivo é evitar duplicação de código e manter essas funções de apoio centralizadas em um único local.

### `data`

Contém os arquivos utilizados para persistência dos dados do sistema.

---

## Fluxo entre as camadas

De forma simplificada:


Usuário
  ↓
Interface
  ↓
Service
  ↓
Repository
  ↓
JSON


No caminho inverso:


JSON
  ↓
Repository
  ↓
Service
  ↓
Interface
  ↓
Usuário


Cada camada possui uma responsabilidade diferente.

---

## Requisitos

- Python 3

Esta versão utiliza apenas recursos da biblioteca padrão do Python e não exige, atualmente, instalação adicional de bibliotecas externas.

Por isso, um arquivo `requirements.txt` não é necessário enquanto não houver dependências de terceiros.

---

## Como executar

Clone o repositório:


git clone https://github.com/LevysLK/sistema-gerenciamento-pedidos


Entre na pasta do projeto:

cd sistema-gerenciamento-pedidos


Execute:

python -u main.py

Também é possível utilizar:

python main.py

---

## Inicialização

O ponto de entrada da aplicação é:

main.py

A inicialização está encapsulada em uma função `main()` e protegida por:

if __name__ == "__main__":
    main()

---

## Tratamento de erros

O projeto diferencia erros de acordo com sua responsabilidade.

Alguns exemplos:

- `TypeError` para tipos incompatíveis;
- `ValueError` para valores inválidos;
- `KeyError` para determinados registros não encontrados;
- erros relacionados à leitura ou corrupção dos arquivos de persistência.

Sempre que possível, exceções são tratadas na camada que possui contexto suficiente para decidir o que fazer com elas.

A interface fica responsável por transformar determinados erros em mensagens compreensíveis para o usuário.

---

## Validação de entradas

As entradas fornecidas pelo usuário são validadas antes de serem utilizadas pela aplicação.

O projeto possui helpers reutilizáveis para reduzir repetição na interface, incluindo funções responsáveis por:

- repetir solicitações até receber valores válidos;
- capturar determinadas exceções;
- apresentar mensagens apropriadas.

Também são utilizadas validações dentro das próprias entidades para impedir que objetos sejam colocados em estados inválidos.

---

## Estado atual

Esta versão pode ser considerada concluída dentro da arquitetura atual baseada em JSON.

O projeto poderá receber novas versões ou refatorações gerais posteriormente.

Uma evolução planejada é substituir a persistência JSON por um banco de dados relacional, mantendo, sempre que possível, as camadas de domínio, serviços e interface independentes da tecnologia de persistência.

Possíveis evoluções incluem:

- PostgreSQL;
- SQLAlchemy;
- migrations;
- Pydantic;
- testes automatizados mais amplos;
- API utilizando FastAPI.

---

## Objetivo de estudo

Este projeto faz parte do processo de aprendizado e consolidação de conceitos de desenvolvimento Python.

A intenção não é apenas implementar funcionalidades, mas também praticar decisões de arquitetura e refatoração, identificando problemas e melhorando progressivamente a qualidade do código.

O histórico de commits do repositório também registra diversas etapas desse processo, incluindo correções, refatorações e melhorias de encapsulamento, persistência e tratamento de erros.

---

## Tecnologias

- Python 3;
- JSON;
- Programação Orientada a Objetos;
- Git;
- GitHub.

---

## Próximas versões

Uma futura versão poderá migrar a camada de persistência para banco de dados.

A arquitetura atual busca facilitar uma evolução como:


Interface
    ↓
Service
    ↓
Repository
    ↓
PostgreSQL


sem transferir regras de negócio para a camada de banco de dados ou para a interface.

---

## Autor

Projeto desenvolvido por Rafael de Castro como parte de estudos e desenvolvimento de portfólio em Python.

---

# English Version

# Order Management System

A Python order management system operated through a terminal interface, with data currently persisted in JSON files.

The project was developed with a focus on code organization, Object-Oriented Programming, separation of concerns, exception handling, data validation, and safe persistence.

The current version uses JSON files as its storage mechanism. Future versions may replace file-based persistence with a relational database.

---

## About the project

The **Order Management System** allows products and orders to be managed through a terminal interface.

It was developed as a study and portfolio project with the goal of applying Python concepts to a complete application while separating responsibilities between domain, service, repository, and interface layers.

Concepts practiced throughout the project include:

- Object-Oriented Programming;
- encapsulation;
- properties, getters, and setters;
- object composition;
- type hints;
- exception handling and propagation;
- separation of concerns;
- service layer;
- Repository pattern;
- JSON persistence;
- data validation;
- generic functions using `Callable` and `TypeVar`;
- `classmethod`;
- constants and domain states;
- protection of internal collections;
- safer file handling;
- modular project organization.

---

## Features

### Products

The system supports:

- product creation;
- product search;
- product listing;
- product editing;
- name and price validation;
- invalid data protection;
- product existence checks;
- empty repository detection.

Products contain domain-level validation rules for attributes such as name and price.

### Orders

The system supports:

- creating orders;
- associating customer information with orders;
- generating order identifiers;
- searching orders by number;
- listing existing orders;
- adding products to orders;
- removing products from orders;
- controlling item quantities;
- calculating item subtotals;
- calculating order totals;
- selecting payment methods;
- completing orders;
- canceling orders;
- preventing invalid operations on completed or canceled orders;
- exporting orders.

### Order items

Each order item contains information related to a product and its quantity.

Product name and price can be preserved as snapshots from the moment the product was added to the order, preventing later changes to the product catalog from incorrectly changing historical order information.

The internal item collection is also protected against direct external mutation.

### Payment methods

The project supports different payment methods through specialized classes.

The system can:

- list available payment methods;
- select a payment method;
- reconstruct payment methods from persisted data;
- prevent order completion when required conditions are not met.

---

## Data persistence

Data is currently stored in JSON files located inside:


data/


Repositories are responsible for accessing and modifying persisted data.

Other application layers do not need to directly manipulate JSON files.

The general flow is:


Interface
    ↓
Service
    ↓
Repository
    ↓
JSON


This separation makes it possible to replace JSON persistence with a database in the future without rewriting the entire business and interface layers.

---

## Safer JSON writes

The application uses temporary files during write operations.

Instead of immediately overwriting the main file, new data is first written to a temporary file.

Simplified flow:


current data
    ↓
temporary .temp file
    ↓
write completed
    ↓
replace original JSON


If a failure occurs while writing, the main persistence file is not immediately overwritten.

During startup, the system also checks for untreated temporary files and warns the user when necessary.

---

## Corrupted file handling

The system distinguishes between situations such as:

- missing files;
- empty repositories;
- corrupted JSON files.

A corrupted JSON file is not automatically interpreted as an empty repository.

This reduces the risk of existing data being overwritten by a newly generated empty structure.

Detection occurs in the persistence layer, while user-facing error messages remain the responsibility of the interface layer.

---

## Architecture

The project aims to assign each responsibility to a specific layer.

Main structure:


sistema-gerenciamento-pedidos/
│
├── .gitignore
├── main.py
├── README.md
│
├── app/
│   ├── config/
│   ├── domain/
│   ├── interface/
│   ├── repositories/
│   ├── services/
│   └── utils/
│
└── data/


### `config`

Contains application settings and constants.

Centralizing these values reduces duplicated literals and makes future changes easier.

### `domain`

Contains classes representing the core entities and fundamental rules of the system.

Examples include:

- product;
- order;
- order item;
- customer;
- payment methods.

Entities are responsible for protecting their own state and maintaining validity rules.

### `interface`

Responsible for terminal-based user interaction.

It includes:

- menus;
- input functions;
- output messages;
- presentation-level error handling;
- interface-specific helpers.

The interface calls services to perform application operations.

### `repositories`

Responsible for retrieving and persisting data.

The current implementation uses JSON files.

This layer centralizes operations such as:

- reading;
- searching;
- inserting;
- replacing;
- persisting.

Repositories may later be adapted to use a database.

### `services`

Contains use cases and business operations that coordinate objects and repositories.

The service layer is not responsible for:

- calling `input()`;
- printing messages to the user;
- directly manipulating JSON files.

This reduces coupling between application rules and the terminal interface.

### `utils`

Contains reusable utility functions that support different parts of the application.

This directory centralizes auxiliary resources that do not directly belong to business rules, the interface, or repositories, such as JSON file handling, conversions, and generic checks shared by multiple modules.

Its purpose is to reduce code duplication and keep supporting functionality organized in a single place.

### `data`

Contains files used to persist application data.

---

## Layer flow

Simplified application flow:


User
  ↓
Interface
  ↓
Service
  ↓
Repository
  ↓
JSON


And back:

JSON
  ↓
Repository
  ↓
Service
  ↓
Interface
  ↓
User

Each layer has a distinct responsibility.

---

## Requirements

- Python 3

The current version relies only on Python standard-library features and does not currently require third-party dependencies.

For that reason, a `requirements.txt` file is not necessary until external packages are introduced.

---

## Running the project

Clone the repository:

git clone https://github.com/LevysLK/sistema-gerenciamento-pedidos

Enter the project directory:

cd sistema-gerenciamento-pedidos

Run:

python -u main.py

You may also use:

python main.py

---

## Application entry point

The application entry point is:

main.py

Startup is encapsulated inside a `main()` function and protected by:

if __name__ == "__main__":
    main()

---

## Error handling

The project distinguishes errors according to their meaning.

Examples include:

- `TypeError` for incompatible types;
- `ValueError` for invalid values;
- `KeyError` for certain missing records;
- persistence-related errors for invalid or corrupted files.

Whenever possible, exceptions are handled by the layer with enough context to determine the appropriate response.

The interface is responsible for converting certain errors into understandable messages for the user.

---

## Input validation

User input is validated before being consumed by application operations.

The project contains reusable helpers intended to reduce repetitive interface logic, including functions responsible for:

- repeatedly requesting values until valid input is provided;
- handling selected exceptions;
- displaying appropriate messages.

Validation also exists within domain entities to prevent objects from entering invalid states.

---

## Current status

This version can be considered complete within its current JSON-based architecture.

The project may receive future releases and larger refactoring cycles.

One planned evolution is replacing JSON persistence with a relational database while keeping the domain, service, and interface layers as independent as possible from the persistence technology.

Possible future technologies include:

- PostgreSQL;
- SQLAlchemy;
- database migrations;
- Pydantic;
- broader automated testing;
- a FastAPI-based API.

---

## Learning goals

This project is part of an ongoing process of learning and consolidating Python development concepts.

The goal is not only to implement features but also to practice architecture decisions and refactoring by identifying issues and progressively improving code quality.

The repository's commit history also documents several stages of this process, including bug fixes, refactoring, encapsulation improvements, persistence improvements, and exception-handling changes.

---

## Technologies

- Python 3;
- JSON;
- Object-Oriented Programming;
- Git;
- GitHub.

---

## Future versions

A future release may migrate persistence to a relational database.

The current architecture is intended to make an evolution such as:

Interface
    ↓
Service
    ↓
Repository
    ↓
PostgreSQL

possible without moving business rules into the database layer or user interface.

---

## Author

Developed by Rafael de Castro as part of Python studies and portfolio development.
