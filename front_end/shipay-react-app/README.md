# Shipay Front-End Engineer Challenge

Implementacao da funcionalidade de filtro de produtos transacionais da Shipay em uma SPA React com Vite.

## Projeto

Funcionalidades implementadas:

- campo de busca para filtrar produtos por texto;
- filtro dinamico conforme o usuario digita;
- busca case-insensitive;
- tratamento de busca sem resultados exibindo a lista vazia.

## Melhoria sugerida

Embora nao tenha sido solicitado no desafio, eu adicionaria um debounce no input de busca em um cenario real. Isso evitaria recalcular o filtro a cada tecla digitada, reduzindo processamento desnecessario principalmente em listas maiores ou quando a busca depender de chamadas a APIs.

## Como executar

Entre no diretorio da aplicacao:

```bash
cd shipay-react-app
```

Instale as dependencias:

```bash
npm install
```

Execute a aplicacao em modo de desenvolvimento:

```bash
npm run dev
```

## Testes

Os testes automatizados foram escritos com Vitest, React Testing Library, jest-dom e user-event.

Execute os testes com:

```bash
npm test
```

### Cenarios cobertos

1. **Renderizacao inicial da lista**
   - Valida que todos os produtos de `data.js` aparecem quando a tela carrega sem termo de busca.

2. **Filtro dinamico conforme o usuario digita**
   - Simula a digitacao no campo de busca e valida que a lista e atualizada de acordo com o termo informado.

3. **Busca case-insensitive**
   - Valida que a busca encontra produtos mesmo quando o texto digitado usa letras minusculas e os dados possuem letras maiusculas.

4. **Busca sem resultados**
   - Valida que nenhum produto e renderizado quando o termo digitado nao corresponde a nenhum item da lista.
