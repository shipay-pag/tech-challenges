## Questão 1 - Implementação da SPA React

A implementação da funcionalidade de filtro de produtos está no diretório `shipay-react-app`.

Os detalhes de execução, testes, cenários cobertos e melhoria sugerida estão documentados em `shipay-react-app/README.md`.

## Questão 2 - Revisão da PR `UserManagement`

O primeiro ponto que eu levantaria é que o componente está escrito como **class component**. Se o projeto ainda usa esse padrão na maior parte da base, tudo bem seguir com classe. Mas, se o restante já estiver usando componentes funcionais, eu pediria para reescrever usando a abordagem mais atual do React, com hooks, para manter o código consistente.

Sobre o código em si, eu não aprovaria a PR ainda porque existem alguns problemas que afetam o funcionamento do componente.

O principal deles é a atualização direta do estado. No `handleNameChange`, o código faz:

```jsx
this.state.newUserName = event.target.value;
```

Isso não é o fluxo correto no React. Alterar `this.state` diretamente pode deixar a interface desatualizada, porque o React não necessariamente sabe que precisa renderizar de novo. O correto seria usar `setState`.

Também existe um problema no input de nome: ele usa `value={this.state.newUserName}`, mas não tem `onChange`. Como ele é um input controlado, isso faz com que o usuário não consiga digitar normalmente. Mesmo existindo um método `handleNameChange`, ele não está sendo chamado.

Outro ponto importante está no `addUser`. O código usa `users.push(newUser)`, o que também altera diretamente um valor que veio do estado. Além disso, depois disso foi usado `forceUpdate()`, que acaba sendo um sinal de que o estado não está sendo atualizado da forma correta. Nesse caso, o ideal é criar um novo array e atualizar tudo com `setState`.

Um exemplo de como eu ajustaria essa parte:

```jsx
handleNameChange(event) {
  this.setState({ newUserName: event.target.value });
}

handleEmailChange(event) {
  this.setState({ newUserEmail: event.target.value });
}

addUser() {
  const { users, newUserName, newUserEmail } = this.state;

  if (!newUserName.trim() || !newUserEmail.trim()) {
    return;
  }

  const newUser = {
    id: Date.now(),
    name: newUserName.trim(),
    email: newUserEmail.trim(),
  };

  this.setState({
    users: [...users, newUser],
    newUserName: "",
    newUserEmail: "",
  });
}
```

Na renderização da lista, também faltou passar uma `key` para cada item do `map`. Isso pode gerar warning no React e causar problemas quando a lista mudar.

```jsx
{this.state.users.map((user) => (
  <li key={user.id}>
    {user.name} ({user.email})
  </li>
))}
```

Além desses ajustes, eu também adicionaria uma validação simples para não permitir cadastro com nome ou e-mail vazio, limparia os campos depois de adicionar um usuário e evitaria gerar o `id` com base em `users.length + 1`, porque isso pode gerar ids repetidos se algum item for removido no futuro.

## Questão 3 - Bug na listagem de produtos

Pela stack trace, o erro está acontecendo dentro do componente `ProductDisplay`, em algum ponto onde o código tenta executar `.map()` em um valor que está `null`.

O problema provavelmente está em uma lista de produtos que deveria ser um array, mas em algum momento chega como `null`. Um exemplo comum seria algo assim:

```jsx
function ProductDisplay({ products }) {
  return (
    <div>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

Esse código funciona quando `products` é um array, mas quebra se `products` vier como `null`, porque `null` não possui o método `map`.

Isso pode acontecer por alguns motivos: o estado inicial foi definido como `null`, a API retornou `null`, ou o componente foi renderizado antes dos dados carregarem. Como a tela de listagem depende de um array para renderizar os cards, o componente precisa tratar esse caso antes de chamar `.map()`.

Uma correção simples seria garantir que `products` sempre tenha um array como valor padrão:

```jsx
function ProductDisplay({ products = [] }) {
  return (
    <div>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

Se a lista vier de um estado, eu também ajustaria o estado inicial para começar como array vazio:

```jsx
const [products, setProducts] = useState([]);
```

E, se os dados vierem de uma API, também trataria a resposta antes de salvar no estado:

```jsx
setProducts(Array.isArray(response.data) ? response.data : []);
```

Dessa forma, o componente continua renderizando mesmo quando ainda não existem produtos carregados ou quando a API retorna um valor inesperado. Se fizer sentido para a experiência da tela, também pode ser exibida uma mensagem de lista vazia quando `products.length === 0`.

## Questão 4 - Autenticação server side e consumo das APIs

Como a aplicação é server side, eu faria a autenticação no servidor, não no componente React renderizado no browser. As credenciais `access_key` e `secret_key` devem ficar em variáveis de ambiente e nunca serem expostas no front.

A ideia seria criar uma função responsável por buscar o token na rota de autenticação e reutilizar esse token enquanto ele ainda estiver válido, já que a documentação informa que ele dura uma hora.

```js
let cachedToken = null;
let tokenExpiresAt = 0;

async function getShipayAccessToken() {
  const now = Date.now();

  if (cachedToken && now < tokenExpiresAt) {
    return cachedToken;
  }

  const response = await fetch("https://api.acme.com/auth", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      access_key: process.env.SHIPAY_ACCESS_KEY,
      secret_key: process.env.SHIPAY_SECRET_KEY,
    }),
  });

  if (!response.ok) {
    throw new Error("Erro ao autenticar na API da Shipay");
  }

  const data = await response.json();

  cachedToken = data.access_token;
  tokenExpiresAt = now + (data.access_token_expires_in - 60) * 1000;

  return cachedToken;
}
```

Depois disso, as chamadas para os endpoints da API usariam o token no header `Authorization`:

```js
async function getLeadsData() {
  const token = await getShipayAccessToken();

  const response = await fetch("https://api.acme.com/leads", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.json();
}
```

Eu também deixaria uma pequena margem antes do vencimento, por exemplo 60 segundos, para evitar usar um token que está muito perto de expirar.

Para performance, se o formulário precisar consumir vários endpoints que não dependem um do outro, eu faria essas chamadas em paralelo em vez de chamar uma depois da outra:

```js
const [products, channels, settings] = await Promise.all([
  fetchProducts(),
  fetchChannels(),
  fetchSettings(),
]);
```

Além disso, eu manteria o token em cache no servidor para não chamar `/auth` a cada requisição. Para dados auxiliares do formulário que mudam pouco, como listas usadas em selects, também avaliaria um cache curto para reduzir chamadas repetidas à API.

## Questão 5 - Solução com BFF para streaming

Um BFF, ou Backend for Front-end, é uma camada de backend criada para atender melhor uma interface específica. Em vez de fazer cada cliente conversar diretamente com vários microsserviços, o cliente chama o seu BFF, e o BFF fica responsável por buscar, agregar e adaptar os dados para aquele tipo de experiência.

Nesse cenário, eu usaria múltiplos BFFs, um para cada tipo principal de cliente: Web, Mobile e Smart TV. A razão é que cada interface tem necessidades bem diferentes. A Web precisa de mais dados e telas mais completas, o Mobile precisa de respostas menores e mais rápidas, e a Smart TV precisa de uma navegação simples, com foco em reprodução e informações essenciais.

Um desenho simples seria:

```txt
Aplicação Web      -> BFF Web      -> MS Catálogo
Aplicação Mobile   -> BFF Mobile   -> MS Usuários
Aplicação Smart TV -> BFF TV       -> MS Streaming
                                  -> MS Catálogo
                                  -> MS Usuários
```

Na prática, cada BFF poderia consumir os mesmos microsserviços, mas devolver respostas diferentes para cada cliente. Por exemplo, o BFF Web pode montar uma home mais completa, enquanto o BFF Mobile pode devolver uma lista mais enxuta com menos campos.

Sobre a distribuição das responsabilidades:

**a) Renderizar botões e layout da interface**

Essa lógica ficaria no cliente. Cada aplicação conhece melhor seu dispositivo, tamanho de tela, forma de navegação e experiência esperada. O BFF pode ajudar enviando dados já formatados, mas não deveria decidir como o botão é renderizado na tela.

**b) Agregar dados para "Recomendações Personalizadas" na Web**

Eu colocaria essa lógica no BFF Web. Ele pode buscar dados do MS de Catálogo e do MS de Usuários, juntar as informações e devolver uma resposta pronta para a tela Web, que precisa mostrar mais detalhes.

**c) Buscar lista simplificada de "Novos Lançamentos" no Mobile**

Essa lógica ficaria no BFF Mobile. O MS de Catálogo pode ter os dados completos, mas o BFF Mobile deve escolher apenas o que o app precisa, como título, imagem de capa e duração. Isso reduz payload e ajuda no carregamento em conexões mais lentas.

**d) Registrar que o usuário assistiu a um vídeo**

A regra principal deve ficar no microsserviço responsável, provavelmente o MS de Usuários, já que ele gerencia histórico de visualização. O cliente ou o BFF podem disparar a ação, mas a regra de negócio e persistência devem ficar no backend de domínio.

**e) Adaptar a qualidade do stream pela conexão do Mobile**

A parte principal deve ficar no MS de Streaming, porque ele é responsável pela entrega do vídeo. O cliente Mobile também participa informando condições de rede e escolhendo a melhor opção durante a reprodução, mas a lógica de disponibilizar as qualidades e entregar o stream deve ficar no serviço de streaming.

**f) Validar formato de e-mail no cadastro Web**

Eu faria uma validação simples no cliente Web para dar feedback rápido ao usuário. Mesmo assim, essa validação também precisa existir no backend, porque validação só no front não é suficiente para garantir integridade dos dados.
