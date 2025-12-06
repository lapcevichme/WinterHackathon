import { useEffect, useState } from 'react'
import FlappyGame from './games/fbird'
import OsuGame from './games/osu'
import LumberjackGame from './games/Lumberjack'
import SkiRunGame from './games/skiRun'
import { setAccessToken } from './api/api'
import { useStartGame } from './hooks/useStartGame'
import { useSubmitScore } from './hooks/useSubmitScore'
import { useExchangeAuth } from './hooks/useExchangeAuth'
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
type Phase = 'start' | 'playing' | 'result'

const GAME_TITLES: Record<GameTab, string> = {
  flappy: 'Flappy Gift',
  osu: 'osu! lite',
  ski: 'Ski Run',
  lumberjack: 'Ice Lumberjack',
}

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

const parseHashParam = (hash: string, key: string): string | null => {
  const trimmed = hash.startsWith('#') ? hash.slice(1) : hash
  const params = new URLSearchParams(trimmed)
  return params.get(key)
}

function App() {
  const [activeGame, setActiveGame] = useState<GameTab>(() => getInitialGame())
  const [phase, setPhase] = useState<Phase>('start')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [finalScore, setFinalScore] = useState<number | null>(null)
  const [energyLeft, setEnergyLeft] = useState<number | null>(null)
  const [initialSid, setInitialSid] = useState<string | null>(null)
  const [launchCode, setLaunchCode] = useState<string | null>(null)
  const [authorized, setAuthorized] = useState<boolean>(false)

  const startMutation = useStartGame()
  const submitScoreMutation = useSubmitScore()
  const exchangeMutation = useExchangeAuth()
  const { reset: resetStart } = startMutation
  const { reset: resetSubmit } = submitScoreMutation

  useEffect(() => {
    const url = new URL(window.location.href)
    const param = normalizeGameParam(url.searchParams.get('game'))
    if (param) setActiveGame(param)

    const sid = url.searchParams.get('sid')
    setInitialSid(sid)
    if (sid) {
      setSessionId(sid)
    }
    const code = parseHashParam(url.hash, 'code')
    if (code) {
      setLaunchCode(code)
      exchangeMutation.mutate(
        { code },
        {
          onSuccess: (data) => {
            setAccessToken(data.access_token)
            setAuthorized(true)
          },
          onError: () => {
            setAccessToken(null)
            setAuthorized(false)
          },
        },
      )
    }

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

  useEffect(() => {
    setPhase('start')
    setSessionId(null)
    setFinalScore(null)
    setEnergyLeft(null)
    resetStart()
    resetSubmit()
    setAccessToken(null)
    setAuthorized(false)
  }, [activeGame, resetStart, resetSubmit])

  const handleStart = () => {
    setPhase('start')
    setFinalScore(null)
    startMutation.reset()
    submitScoreMutation.reset()
    if (initialSid) {
      setSessionId(initialSid)
      setPhase('playing')
      return
    }
    startMutation.mutate(undefined, {
      onSuccess: (data) => {
        setSessionId(data.session_id)
        setEnergyLeft(data.energy_left)
        setPhase('playing')
      },
    })
  }

  const notifyBridge = (score: number) => {
    if (window.AndroidGame?.sendScore) {
      window.AndroidGame.sendScore(score)
    } else {
      console.log('Score sent:', score)
    }
  }

  const handleExit = () => {
    if (window.AndroidGame?.closeGame) {
      window.AndroidGame.closeGame()
    } else {
      window.close()
    }
    setPhase('start')
    setSessionId(null)
    setFinalScore(null)
    setEnergyLeft(null)
    resetStart()
    resetSubmit()
    setAccessToken(null)
    setAuthorized(false)
  }

  const handleGameFinished = (score: number) => {
    setFinalScore(score)
    if (sessionId) {
      submitScoreMutation.mutate({ session_id: sessionId, score })
    }
    notifyBridge(score)
    setPhase('result')
  }

  return (
    <div className="app">
      <div className="canvas-wrapper">
        {phase === 'playing' && (
          <>
            {activeGame === 'flappy' && <FlappyGame onSendScore={handleGameFinished} />}
            {activeGame === 'osu' && <OsuGame onSendScore={handleGameFinished} />}
            {activeGame === 'ski' && <SkiRunGame onSendScore={handleGameFinished} />}
            {activeGame === 'lumberjack' && <LumberjackGame onSendScore={handleGameFinished} />}
          </>
        )}
      </div>
      {phase === 'start' && (
        <div className="overlay">
          <div className="overlay-card">
            <div className="overlay-label">Winter Hackathon</div>
            <h1 className="overlay-title">{GAME_TITLES[activeGame]}</h1>
            <p className="overlay-subtitle">Начните новую попытку, мы спишем энергию на стороне сервера.</p>
            {!authorized && (
              <div className="overlay-error">
                {!launchCode
                  ? 'Нет launch code в URL (#code=...). Откройте игру из приложения.'
                  : exchangeMutation.isPending
                    ? 'Авторизуемся…'
                    : 'Не удалось авторизоваться. Попробуйте перезапустить из приложения.'}
              </div>
            )}
            {energyLeft !== null && (
              <div className="stat-pill">Энергия после прошлой попытки: {energyLeft}</div>
            )}
            {startMutation.error && (
              <div className="overlay-error">
                Не удалось запустить сессию: {startMutation.error.message}
              </div>
            )}
            <div className="overlay-actions">
              <button
                className="btn primary"
                onClick={handleStart}
                disabled={startMutation.isPending || !authorized}
              >
                {startMutation.isPending ? 'Запускаем…' : 'Начать игру'}
              </button>
            </div>
          </div>
        </div>
      )}
      {phase === 'result' && (
        <div className="overlay">
          <div className="overlay-card">
            <div className="overlay-label">Результат</div>
            <h1 className="overlay-title">Счёт: {finalScore ?? 0}</h1>
            {submitScoreMutation.isPending && <p className="overlay-subtitle">Отправляем результат…</p>}
            {submitScoreMutation.isSuccess && (
              <div className="stat-grid">
                <div className="stat-pill">
                  Команде добавлено: {submitScoreMutation.data.team_score_added}
                </div>
                <div className="stat-pill">
                  Итоговый командный счёт: {submitScoreMutation.data.total_team_score}
                </div>
              </div>
            )}
            {submitScoreMutation.error && (
              <div className="overlay-error">
                Не вышло отправить результат: {submitScoreMutation.error.message}
              </div>
            )}
            <div className="overlay-actions">
              <button className="btn primary" onClick={handleStart} disabled={startMutation.isPending}>
                {startMutation.isPending ? 'Запускаем…' : 'Играть снова'}
              </button>
              <button className="btn secondary" onClick={handleExit}>
                В меню
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
