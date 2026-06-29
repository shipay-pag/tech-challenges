# Shipay Front-End Engineer Challenge

Implementação da funcionalidade de filtro de produtos transacionais da Shipay em uma SPA React com Vite.

## Projeto

Funcionalidades implementadas:

- campo de busca para filtrar produtos por texto;
- filtro dinâmico conforme o usuário digita;
- busca case-insensitive;
- tratamento de busca sem resultados exibindo a lista vazia.

## Melhoria sugerida

Embora não tenha sido solicitado no desafio, eu adicionaria um debounce no input de busca em um cenário real. Isso evitaria recalcular o filtro a cada tecla digitada, reduzindo processamento desnecessário principalmente em listas maiores ou quando a busca depender de chamadas a APIs.

## Como executar

Entre no diretório da aplicação:

```bash
cd shipay-react-app
```

Instale as dependências:

```bash
npm install
```

Execute a aplicação em modo de desenvolvimento:

```bash
npm run dev
```

## Testes

Os testes automatizados foram escritos com Vitest, React Testing Library, jest-dom e user-event.

Execute os testes com:

```bash
npm test
```

### Cenários cobertos

1. **Renderização inicial da lista**
   - Valida que todos os produtos de `data.js` aparecem quando a tela carrega sem termo de busca.

2. **Filtro dinâmico conforme o usuário digita**
   - Simula a digitação no campo de busca e valida que a lista é atualizada de acordo com o termo informado.

3. **Busca case-insensitive**
   - Valida que a busca encontra produtos mesmo quando o texto digitado usa letras minúsculas e os dados possuem letras maiúsculas.

4. **Busca sem resultados**
   - Valida que nenhum produto é renderizado quando o termo digitado não corresponde a nenhum item da lista.
