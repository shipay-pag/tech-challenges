import { useState } from 'react';
import initialItems from './data'; // Mock data
import './App.css';

function ProductSearch({ value, onChange }) {
  return (
    <label className="search-field">
      Buscar produto
      <input
        type="text"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Digite o nome do produto"
      />
    </label>
  );
}

function ProductList({ items }) {
  return (
    <ul className="product-list">
      {items.map((item) => (
        <li className="product-list-item" key={item.id}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const normalizedSearchTerm = searchTerm.trim().toLowerCase();

  const filteredItems = initialItems.filter((item) =>
    item.name.toLowerCase().includes(normalizedSearchTerm)
  );

  return (
    <main className="app">
      <section className="product-section" aria-labelledby="product-list-title">
        <h1 id="product-list-title">Produtos transacionais Shipay</h1>

        <ProductSearch value={searchTerm} onChange={setSearchTerm} />
        <ProductList items={filteredItems} />
      </section>
    </main>
  );
}

export default App;
