import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx' // Make sure your file is capitalized as App.jsx, not app.jsx!
import './main.css'         // <-- CHANGED THIS LINE

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)