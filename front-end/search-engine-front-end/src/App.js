import React, { useEffect } from 'react'
import {useState} from 'react';
import axios from 'axios'
import './style.css'

function App() {
  const [data, setData] = useState('')
  const [linkData, setLinkData] = useState([{}]);

  const fetchData =  async () => {

     fetch("/search", {
        headers : { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
      }).then(
        (res) => res.json()
    ).then(
      (links) => {
          setLinkData(links)
          console.log(links)
        }
    )
  }

  return (
    <div className='background'>
    <div className="App">
      <h1>LOOK UP</h1>
      <h2>ENTER PHRASE</h2>
      <div className='button-row'>
        <input
          placeholder='ENTER PHRASE'
          type = "text"
          value = {data}
          required
          onChange={(e) => setData(e.target.value)}/>
        <button onClick={fetchData}>SEARCH</button>
      </div>
      <div>
        {(typeof linkData.links === 'undefined') ? (
            <p></p>
        ) :   (          
        linkData.links.map(
          (link,index) =><div className="singleResult" key={link.link}>{index+1}. <a>{link.link}</a></div>
        ))
        }
      </div>
      </div>
    </div>
  );
}

export default App;
