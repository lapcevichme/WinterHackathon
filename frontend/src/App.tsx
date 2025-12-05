import { useEffect, useState } from 'react'
import FlappyGame from './games/fbird'
import OsuGame from './games/osu'
import LumberjackGame from './games/Lumberjack'
import SkiRunGame from './games/skiRun'
import './App.css'

declare global {
  interface Window {
    AndroidGame?: {
      sendScore: (score: number) => void
      closeGame?: () => void
    }
    setGameFromApp?: (game: string) => void
  }
}

type GameTab = 'flappy' | 'osu' | 'ski' | 'lumberjack'

const normalizeGameParam = (value: string | null): GameTab | null => {
  if (!value) return null
  const key = value.toLowerCase()
  if (key === 'flappy') return 'flappy'
  if (key === 'osu') return 'osu'
  if (key === 'ski' || key === 'skirun') return 'ski'
  if (key === 'lumberjack' || key === 'ice-lumberjack') return 'lumberjack'
  return null
}

const getInitialGame = (): GameTab => {
  const fromQuery = normalizeGameParam(new URLSearchParams(window.location.search).get('game'))
  return fromQuery ?? 'flappy'
}

function App() {
  const [activeGame, setActiveGame] = useState<GameTab>(() => getInitialGame())

  useEffect(() => {
    const param = normalizeGameParam(new URLSearchParams(window.location.search).get('game'))
    if (param) setActiveGame(param)

    window.setGameFromApp = (game: string) => {
      const next = normalizeGameParam(game)
      if (next) setActiveGame(next)
    }

    const onMessage = (event: MessageEvent) => {
      const payload = event.data
      const candidate = normalizeGameParam(
        typeof payload === 'string' ? payload : payload?.game ?? payload?.type,
      )
      if (candidate) setActiveGame(candidate)
    }
    window.addEventListener('message', onMessage)

    return () => {
      delete window.setGameFromApp
      window.removeEventListener('message', onMessage)
    }
  }, [])

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    params.set('game', activeGame)
    const url = `${window.location.pathname}?${params.toString()}${window.location.hash}`
    window.history.replaceState({}, '', url)
  }, [activeGame])

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
      <div className="canvas-wrapper">
        {activeGame === 'flappy' && <FlappyGame onSendScore={sendScore} />}
        {activeGame === 'osu' && <OsuGame onSendScore={sendScore} />}
        {activeGame === 'ski' && <SkiRunGame onSendScore={sendScore} />}
        {activeGame === 'lumberjack' && <LumberjackGame onSendScore={sendScore} />}
      </div>
    </div>
  )
}

export default App
