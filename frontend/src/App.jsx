import { useState } from 'react'
import './App.css'
import FruitList from './components/Fruits';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>Fruit Management App</h1>
      </header>
      <main>
        <FruitList />
      </main>
    </div>
  );
}

export default App
