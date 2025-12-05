import { useState } from 'react'
import FlappyGame from './games/fbird'
import OsuGame from './games/osu'
import SkiRunGame from './games/skiRun'
import './App.css'

declare global {
  interface Window {
    AndroidGame?: {
      sendScore: (score: number) => void
      closeGame?: () => void
    }
  }
}

type GameTab = 'flappy' | 'osu' | 'ski'

function App() {
  const [activeGame, setActiveGame] = useState<GameTab>('flappy')

  const sendScore = (finalScore: number) => {
    if (window.AndroidGame?.sendScore) {
      window.AndroidGame.sendScore(finalScore)
    } else {
      console.log('Android bridge not found. Score:', finalScore)
      alert(`Очки отправлены: ${finalScore}`)
    }
  }

  return (
    <div className="app">
      <div className="topbar">
        <button
          className={`tab ${activeGame === 'flappy' ? 'active' : ''}`}
          onClick={() => setActiveGame('flappy')}
        >
          Flappy Bird
        </button>
        <button
          className={`tab ${activeGame === 'osu' ? 'active' : ''}`}
          onClick={() => setActiveGame('osu')}
        >
          osu! lite
        </button>
        <button
          className={`tab ${activeGame === 'ski' ? 'active' : ''}`}
          onClick={() => setActiveGame('ski')}
        >
          Ski run
        </button>
      </div>

      <div className="canvas-wrapper">
        {activeGame === 'flappy' && <FlappyGame onSendScore={sendScore} />}
        {activeGame === 'osu' && <OsuGame onSendScore={sendScore} />}
        {activeGame === 'ski' && <SkiRunGame onSendScore={sendScore} />}
      </div>
    </div>
  )
}

export default App
