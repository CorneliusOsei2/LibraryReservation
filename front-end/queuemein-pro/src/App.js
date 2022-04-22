import './App.css';
import React, {useState} from 'react';


function App() {

  const [weeks, setWeeks] = useState([]);
  
  const genWeeks = () => {
    fetch("http://127.0.0.1:5500/library/weeks/", {
      "methods" : "GET",
      headers: {
        "Content-Type": "applications/json"
      }
      })
      .then(res => res.json())
      .then(res => setWeeks(res.weeks))
      .catch(err => console.log(err))
  };

 console.log(weeks);
  return (
    <div className="App">
      <header className="App-header">
        
        <button onClick={genWeeks}>Weeks</button>
        
          <div className='row'>
            
          
            {weeks.map(wk => {
              return (
              <div className='card col-md-3' key={wk.id}>
                <div className='card-title'> {wk.number} </div>
              </div>
            )}
            )
            }
        </div>
      </header>
    </div>
  );
}

export default App;
