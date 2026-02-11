# Shipay Techlead Front-End Engineer Challenge

**Objetivo**

Avaliar a visão arquitetural, tomada de decisão e a capacidade de criar abstrações escaláveis. O foco é a qualidade das definições e trade-offs em vez do volume de código produzido.

**Formato da Entrega**

* Repositório de código fonte (Monorepo ou estrutura simplificada).
* README Estratégico: Explicando as escolhas técnicas, como a solução escala e como os times colaborariam.
* Diagrama de Arquitetura: Representação visual do ecossistema proposto (pode ser imagem ou link para ferramenta como Excalidraw/Mermaid).
* Encaminhar as soluções das questões para o endereço de e-mail: avalia@shipay.com.br

**Critérios de Avaliação**
1. **Arquitetura e Trade-offs:** A clareza no README sobre por que escolheu determinada estratégia de Microfrontends e SSR.
2. **Qualidade de Abstração:** Como os tokens e as interfaces (Props) dos componentes foram desenhados.
3. **Pragmatismo:** Capacidade de entregar uma solução funcional sem "overengineering".
4. **Boas Práticas:** Organização do código, legibilidade e conceitos básicos de acessibilidade.


**Desafios**

**1.- Estratégia de Microfrontends & SSR**

Foi atribuído a você, o desenvolvimento de um painel CMS (Sistema de Gerenciamento de Conteúdos) White Label, que permitirá a customização da identidade visual pelos nosso clientes.
Em vez de configurar múltiplos servidores, você deve criar uma aplicação base (Shell) utilizando um framework com suporte a SSR (ex: Next.js).

* **Tarefa:** Implementar uma página que simule a recepção de um parâmetro de "Tenant" (via URL ou Cookie).
* **Requisito Técnico:** Demonstrar como o SSR lida com a identidade visual (White Label) de dois clientes diferentes (ex: Cliente A e Cliente B), alterando minimamente um logotipo e uma cor primária.
* **Documentação:**
* + ***Contexto para a questão: Sabendo que o tema Micro Front-End é um assunto complexo, e limitando o escopo da questão por ser uma avaliação, por favor imagine que a contrução do painel CMS será dividida entre times de desenvolvimento, e que cada time possui funcionalidades características de um produto distinto do outro dentro de um portfólio da empresa.***
* + Questão: Descreva como você organizaria a infraestrutura para que outros times pudessem plugar "Remote Apps" (ex: um microfrontend de pagamentos) nesse Shell.

\
  \
**2.- Design System & Escalabilidade**

Proponha a base de um sistema de design que suporte múltiplos tenants e múltiplos times.

* **Tarefa:** Criar uma estrutura de Design Tokens (JSON ou variáveis CSS) e implementar um único componente (ex: um Botão ou Card) que consuma esses tokens.
* **Ponto de Atenção:** Como você garantiria que uma mudança no Design System não quebrasse os microfrontends que o utilizam? (Explique brevemente sua estratégia de versionamento e governança no README).

\
  \
**3.- Abstração de Componentes Complexos (Gráficos)**

Avalia-se aqui como você desenha APIs de componentes para serem usados por outros desenvolvedores.

* **Tarefa:** Definir a interface (TypeScript) e uma implementação básica de um componente de gráfico reutilizável. Não é necessário configurar bibliotecas complexas; você pode usar um gráfico de barras simples em CSS ou uma lib rápida (ex: Recharts) com dados mockados.
* **Foco:** O componente deve ser agnóstico ao provedor de dados e permitir fácil customização de estados (Loading, Empty, Error).

BOA SORTE!
