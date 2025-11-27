import { useEffect, useRef, useState } from 'react'
import './App.css'

declare global {
  interface Window {
    AndroidGame?: {
      sendScore: (score: number) => void
      closeGame?: () => void
    }
  }
}

type GameState = 'ready' | 'playing' | 'over'

type Pipe = {
  x: number
  gapY: number
  passed: boolean
}

const GRAVITY = 0.45
const FLAP_STRENGTH = -7.5
const BASE_SPEED = 2.8

function App() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [gameState, setGameState] = useState<GameState>('ready')
  const [score, setScore] = useState(0)

  const requestRef = useRef<number | null>(null)
  const lastTimeRef = useRef<number>(0)
  const birdRef = useRef<{ y: number; vy: number }>({ y: 0, vy: 0 })
  const pipesRef = useRef<Pipe[]>([])
  const stateRef = useRef<GameState>('ready')
  const scoreRefInternal = useRef(0)

  useEffect(() => {
    stateRef.current = gameState
  }, [gameState])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const resize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
      if (stateRef.current === 'ready') {
        birdRef.current = { y: canvas.height * 0.5, vy: 0 }
        pipesRef.current = []
      }
      drawScene()
    }

    resize()
    window.addEventListener('resize', resize)
    const onKeyDown = (event: KeyboardEvent) => {
      const currentState = stateRef.current
      if (event.code === 'Space' || event.code === 'ArrowUp') {
        event.preventDefault()
        handleInput()
      }
      if (event.code === 'KeyR' && currentState === 'over') {
        event.preventDefault()
        startGame()
      }
    }
    window.addEventListener('keydown', onKeyDown)

    return () => {
      window.removeEventListener('resize', resize)
      window.removeEventListener('keydown', onKeyDown)
      if (requestRef.current) cancelAnimationFrame(requestRef.current)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleInput = () => {
    if (stateRef.current === 'ready') {
      startGame()
      return
    }
    if (stateRef.current === 'playing') {
      flap()
      return
    }
    if (stateRef.current === 'over') {
      startGame()
    }
  }

  const flap = () => {
    birdRef.current.vy = FLAP_STRENGTH
  }

  const startGame = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const height = canvas.height
    birdRef.current = { y: height * 0.5, vy: 0 }
    pipesRef.current = []
    setScore(0)
    scoreRefInternal.current = 0
    setGameState('playing')

    spawnPipe()
    lastTimeRef.current = performance.now()
    if (requestRef.current) cancelAnimationFrame(requestRef.current)
    requestRef.current = requestAnimationFrame(tick)
  }

  const endGame = (finalScore: number) => {
    if (stateRef.current === 'over') return
    setGameState('over')
    if (requestRef.current) cancelAnimationFrame(requestRef.current)
    sendScore(finalScore)
  }

  const sendScore = (finalScore: number) => {
    if (window.AndroidGame?.sendScore) {
      window.AndroidGame.sendScore(finalScore)
    } else {
      console.log('Android bridge not found. Score:', finalScore)
      alert(`Очки отправлены: ${finalScore}`)
    }
  }

  const spawnPipe = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const height = canvas.height
    const pipeWidth = Math.max(68, Math.min(90, canvas.width * 0.18))
    const gapHeight = Math.max(150, Math.min(220, height * 0.25))
    const margin = Math.max(60, height * 0.12)
    const maxGapStart = height - gapHeight - margin
    const gapY =
      margin + Math.random() * Math.max(10, maxGapStart - margin)

    pipesRef.current.push({
      x: canvas.width + pipeWidth,
      gapY,
      passed: false,
    })
  }

  const tick = (timestamp: number) => {
    const delta = Math.min(timestamp - lastTimeRef.current, 32)
    lastTimeRef.current = timestamp

    update(delta)
    drawScene()

    if (stateRef.current === 'playing') {
      requestRef.current = requestAnimationFrame(tick)
    }
  }

  const update = (delta: number) => {
    const canvas = canvasRef.current
    if (!canvas) return

    const width = canvas.width
    const height = canvas.height
    const dt = delta / (1000 / 60)
    const birdX = width * 0.25
    const birdRadius = Math.max(14, Math.min(18, height * 0.025))
    const pipeWidth = Math.max(68, Math.min(90, width * 0.18))
    const pipeSpacing = Math.max(240, width * 0.48)
    const gapHeight = Math.max(150, Math.min(220, height * 0.25))

    const bird = birdRef.current
    bird.vy += GRAVITY * dt
    bird.y += bird.vy * dt

    const pipes = pipesRef.current

    if (!pipes.length || pipes[pipes.length - 1].x < width - pipeSpacing) {
      spawnPipe()
    }

    pipes.forEach((pipe) => {
      pipe.x -= BASE_SPEED * dt
      if (!pipe.passed && pipe.x + pipeWidth < birdX - birdRadius) {
        pipe.passed = true
        setScore((prev) => {
          const next = prev + 1
          scoreRefInternal.current = next
          return next
        })
      }
    })

    while (pipes.length && pipes[0].x + pipeWidth < 0) {
      pipes.shift()
    }

    const hitTopOrBottom =
      bird.y - birdRadius <= 0 || bird.y + birdRadius >= height
    if (hitTopOrBottom) {
      endGame(scoreRef())
      return
    }

    const hitPipe = pipes.some((pipe) => {
      const withinPipe =
        birdX + birdRadius > pipe.x && birdX - birdRadius < pipe.x + pipeWidth
      const inGap =
        bird.y - birdRadius > pipe.gapY &&
        bird.y + birdRadius < pipe.gapY + gapHeight
      return withinPipe && !inGap
    })

    if (hitPipe) {
      endGame(scoreRef())
    }
  }

  const scoreRef = () => scoreRefInternal.current
  useEffect(() => {
    scoreRefInternal.current = score
  }, [score])

  const drawScene = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const { width, height } = canvas
    const pipes = pipesRef.current
    const bird = birdRef.current
    const birdX = width * 0.25
    const birdRadius = Math.max(14, Math.min(18, height * 0.025))
    const pipeWidth = Math.max(68, Math.min(90, width * 0.18))
    const gapHeight = Math.max(150, Math.min(220, height * 0.25))

    const gradient = ctx.createLinearGradient(0, 0, 0, height)
    gradient.addColorStop(0, '#0f172a')
    gradient.addColorStop(1, '#0b2644')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, width, height)

    pipes.forEach((pipe) => {
      drawPipe(ctx, pipe, pipeWidth, gapHeight, height)
    })

    drawBird(ctx, birdX, bird.y, birdRadius, bird.vy)
    drawGround(ctx, height)
  }

  const drawPipe = (
    ctx: CanvasRenderingContext2D,
    pipe: Pipe,
    width: number,
    gapHeight: number,
    canvasHeight: number,
  ) => {
    ctx.fillStyle = '#1cb66f'
    ctx.strokeStyle = '#0f8e51'
    ctx.lineWidth = 6

    ctx.fillRect(pipe.x, 0, width, pipe.gapY)
    ctx.strokeRect(pipe.x, 0, width, pipe.gapY)

    const bottomHeight = canvasHeight - (pipe.gapY + gapHeight)
    ctx.fillRect(pipe.x, pipe.gapY + gapHeight, width, bottomHeight)
    ctx.strokeRect(pipe.x, pipe.gapY + gapHeight, width, bottomHeight)
  }

  const drawBird = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    radius: number,
    vy: number,
  ) => {
    ctx.save()
    const tilt = Math.max(-0.35, Math.min(0.35, vy / 10))
    ctx.translate(x, y)
    ctx.rotate(tilt)

    ctx.fillStyle = '#fbbf24'
    ctx.beginPath()
    ctx.arc(0, 0, radius, 0, Math.PI * 2)
    ctx.fill()

    ctx.fillStyle = '#f59e0b'
    ctx.beginPath()
    ctx.arc(-radius * 0.25, radius * 0.1, radius * 0.65, 0, Math.PI * 2)
    ctx.fill()

    ctx.fillStyle = '#fff'
    ctx.beginPath()
    ctx.arc(radius * 0.35, -radius * 0.2, radius * 0.35, 0, Math.PI * 2)
    ctx.fill()
    ctx.fillStyle = '#0f172a'
    ctx.beginPath()
    ctx.arc(radius * 0.35, -radius * 0.2, radius * 0.16, 0, Math.PI * 2)
    ctx.fill()

    ctx.fillStyle = '#e11d48'
    ctx.beginPath()
    ctx.moveTo(radius * 0.9, radius * 0.05)
    ctx.lineTo(radius * 1.35, 0)
    ctx.lineTo(radius * 0.9, -radius * 0.05)
    ctx.closePath()
    ctx.fill()

    ctx.restore()
  }

  const drawGround = (ctx: CanvasRenderingContext2D, canvasHeight: number) => {
    const groundHeight = Math.max(20, canvasHeight * 0.06)
    const y = canvasHeight - groundHeight
    const gradient = ctx.createLinearGradient(0, y, 0, canvasHeight)
    gradient.addColorStop(0, '#0f8e51')
    gradient.addColorStop(1, '#0c6b3e')
    ctx.fillStyle = gradient
    ctx.fillRect(0, y, ctx.canvas.width, groundHeight)
  }

  return (
    <div className="app" onPointerDown={handleInput}>
      <canvas ref={canvasRef} className="game-canvas" />
      <div className="hud">
        <div className="score-badge">Счёт: {score}</div>
        {gameState === 'ready' && (
          <div className="message">Тапни или нажми пробел, чтобы взлететь</div>
        )}
        {gameState === 'over' && (
          <div className="message">
            Игра окончена. Тапни, чтобы начать заново
          </div>
        )}
      </div>
    </div>
  )
}

export default App
