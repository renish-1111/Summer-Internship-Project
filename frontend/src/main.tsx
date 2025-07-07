import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import ClickSpark from './ui/ClickSpark.tsx'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
  
    <ClickSpark
    // purpul
    sparkColor="#a855f7"
    sparkSize={11}
    sparkRadius={15}
    sparkCount={8}
    duration={500}
    easing="ease-out"
    extraScale={2.0}
    >
    <App />
    </ClickSpark>
      
  </StrictMode>,
)
