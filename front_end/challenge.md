# Shipay Front-End Engineer Challenge

***Nota: Utilizaremos os seguintes critérios para a avaliação: Desempenho, Testes, Manutenabilidade e boas práticas de engenharia de software.***

**1.- Você recebeu uma atividade para adicionar uma funcionalidade em uma página SPA React simples que lista uma coleção de itens (os produtos transacionais da Shipay). Sua tarefa é implementar a seguinte funcionalidade:**

**Funcionalidade a ser desenvolvida:** Filtro de itens por texto.

**Requisitos:**  

    a. Adicione um campo de input de texto na tela onde a lista é exibida;  
    b. À medida que o usuário digita nesse campo, a lista de itens deve ser filtrada dinamicamente para exibir apenas os itens cujo nome/título contenha o texto digitado;  
    c. A filtragem deve ser case-insensitive (ignorar maiúsculas/minúsculas);  
    d. Mantenha a estrutura de componentes existente, criando novos componentes se julgar necessário;  
    e. Preocupe-se com a clareza do código, boas práticas de React (uso de estado, props, hooks como ```useState``` e ```useEffect``` de forma apropriada) e componentização;  

***Nota: Você pode utilizar o scaffold disponibilizado no diretório "shipay-react-app" ou sugerir uma estrutura mais adequada. O que achar melhor.***  

**2.- Seu colega solicitou a avaliação de uma Pull Request para que ele possa seguir com o deploy para os testes em Sandbox. Por favor, avalie a PR e faça as ponderações pertinentes, se necessário.**

**Código para Revisão:**  

```JavaScript
# Linguagem: React

// UserManagement.js
import React from 'react';

class UserManagement extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      users: [
        { id: 1, name: 'Alice', email: 'alice@example.com' },
        { id: 2, name: 'Bob', email: 'bob@example.com' }
      ],
      newUserName: '',
      newUserEmail: ''
    };
  }

  handleNameChange(event) {
    this.state.newUserName = event.target.value;
  }

  handleEmailChange(event) {
    this.setState({ newUserEmail: event.target.value });
  }

  addUser() {
    const newUser = {
      id: this.state.users.length + 1,
      name: this.state.newUserName,
      email: this.state.newUserEmail
    };

    this.state.users.push(newUser);
    this.forceUpdate();

  }

  render() {
    return (
      <div>
        <h2>Gerenciamento de Usuários</h2>
        <div>
          <input
            type="text"
            placeholder="Nome do usuário"
            value={this.state.newUserName}
          />
          <input
            type="email"
            placeholder="Email do usuário"
            value={this.state.newUserEmail}
            onChange={(e) => this.handleEmailChange(e)}
          />
          <button onClick={() => this.addUser()}>Adicionar Usuário</button>
        </div>
        <ul>
          {this.state.users.map(user => (
            <li>
              {user.name} ({user.email})
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default UserManagement;

```

**3.- Nossos analistas de qualidade reportaram uma falha na página de listagem de produtos Shipay. Um card reportando o bug foi atribuído à você com a ***Stack Trace*** a seguir.**

```
TypeError: Cannot read properties of null (reading 'map')
  at ProductDisplay (http://localhost:3000/static/js/main.chunk.js:XXX:YY)
  at renderWithHooks (http://localhost:3000/static/js/vendors~main.chunk.js:AAAA:BB)
  at mountIndeterminateComponent (http://localhost:3000/static/js/vendors~main.chunk.js:BBBB:CC)
  ... (outras linhas do stack trace)
```

Baseado na stack trace, sua tarefa é:  
- Identificar a causa do problema no código.  
- Explicar qual é o problema.  
- Sugerir a correção para o código.  
  


**4.- Você ficou responsável por desenvolver um componente que será utilizado por uma aplicação Server Side em React. Essa aplicação irá consumir alguns endpoints de APIs para manipular informações de um formulário de cadastro de oportunidades de vendas (Leads) para novos clientes.  
Os endpoints da API por serem expostos publicamente, solicitam um token OAuth JWT com duração de uma hora. Consultando a documentação disponibilizada a seguir, sugira a implementação da autenticação e geração do token JWT para ser utilizada pela aplicação/formulário server side.
O que você poderia propor para otimização de performance no caso do consumo de múltiplos endpoints da API para a utilização do formulário de leads?**


```
Autenticação para acesso aos serviços transacionais.

Este serviço gera um token de acesso para utilizar às APIs transacionais da Shipay.

Requisição:
POST - https://api.acme.com/auth
Para gerar o token de acesso, é necessário o envio das seguintes credenciais na requisição:
access_key - **string - Ex.: DFt7Oqzn_LGyYnDGLwX7oA**
secret_key - **string - Ex.: dNiIFM34DSvKIAubw9nfJL7qrFWFoYKLSeHTPVOyNcEBw-7oTROVK3mq5mbzR_h_emcxZAaWyjmFsd7TVdeBmZ**

Possíveis Respostas:
HTTP 200
Authenticated.

Response body
access_token - string
Token de acesso do sistema autenticado.

access_token_expires_in - integer
Tempo de vida em segundos do token de acesso.

refresh_token - string
Token de atualização do sistema autenticado.

refresh_token_expires_in - integer
Tempo de vida em segundos do token de atualização.

HTTP 401
Unauthenticated.

Response body
code - integer
Código de erro.

message - string
Mensagem de erro.
```


**5.- Imagine que você trabalha em uma empresa de streaming de vídeos. A empresa deseja aprimorar e expandir suas interfaces de cliente e precisa que você desenhe uma solução utilizando o padrão Back for Front-end (BFF).**

Atualmente, a empresa possui os seguintes microsserviços (MS) no back-end:  
  
MS de Catálogo: Fornece informações sobre filmes e séries (título, sinopse, elenco, classificações, etc.).  
MS de Usuários: Gerencia dados dos usuários (perfis, preferências, histórico de visualização).  
MS de Streaming: Responsável pela entrega do vídeo em si.  

As interfaces de cliente são:  
  
a. Aplicação Web: Deve exibir uma grande quantidade de informações do catálogo na tela inicial, recomendações personalizadas e histórico detalhado.  
b. Aplicação Mobile (iOS/Android): Deve ter uma interface mais leve, otimizada para telas menores e conexões de dados potencialmente mais lentas, focando em funcionalidades essenciais e carregamento rápido de listas de vídeos.  
c. Aplicação para Smart TVs: Precisa de uma navegação simples, otimizada para controle remoto, e foco na qualidade de imagem e informações essenciais do vídeo antes da reprodução.  

Considerando o cenário acima, por favor, responda às seguintes perguntas:  

Conceito do BFF: Explique resumidamente o que é um Back for Front-end e qual seria o principal papel e benefícios de implementar um (ou mais) BFFs nesta situação para a empresa de streaming.  

Design da Solução: Você implementaria um único BFF para todos os clientes ou múltiplos BFFs? Justifique sua escolha.  
Esboce um diagrama simples mostrando como os clientes (Web, Mobile, Smart TV), o(s) BFF(s) e os microsserviços existentes se conectariam.  

Distribuição de Lógicas e Responsabilidades: Para cada um dos exemplos de lógica/tarefa abaixo, indique onde você acredita que ela seria predominantemente implementada (no cliente, no BFF ou nos microsserviços de back-end) e justifique brevemente:  
a) Lógica para renderizar os botões e o layout da interface do usuário em cada dispositivo.  
b) Lógica para agregar dados do MS de Catálogo e do MS de Usuários para montar a tela de "Recomendações Personalizadas" para a versão Web, que exibe muitos detalhes.  
c) Lógica para buscar uma lista simplificada de "Novos Lançamentos" para a aplicação Mobile, contendo apenas título, imagem de capa e duração.  
d) Lógica de negócio principal para registrar que um usuário assistiu a um vídeo (atualizar histórico).  
e) Lógica para adaptar a qualidade do stream de vídeo (MS de Streaming) com base na velocidade da conexão do usuário Mobile.  
f) Validação de formato de e-mail no formulário de cadastro no cliente Web.  

BOA SORTE!
