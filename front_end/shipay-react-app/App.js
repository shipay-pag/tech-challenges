import initialItems from './data'; // Mock data
import './App.css';

function App() {
  return (
    <main className="app">
      <section className="product-section" aria-labelledby="product-list-title">
        <h1 id="product-list-title">Produtos transacionais Shipay</h1>

        <ul className="product-list">
          {initialItems.map((item) => (
            <li className="product-list-item" key={item.id}>
              {item.name}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}

export default App;
