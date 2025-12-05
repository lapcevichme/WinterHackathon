import { useEffect, useRef, useState } from 'react'

type GameState = 'ready' | 'playing' | 'over'

type Pipe = {
  x: number
  gapY: number
  passed: boolean
}

type SnowFlake = {
  x: number
  y: number
  radius: number
  speed: number
  sway: number
  phase: number
  opacity: number
  layer: number
}

type FlappyProps = {
  onSendScore: (score: number) => void
}

const GRAVITY = 0.45
const FLAP_STRENGTH = -7.5
const BASE_SPEED = 2.8

function FlappyGame({ onSendScore }: FlappyProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [state, setState] = useState<GameState>('ready')
  const [score, setScore] = useState(0)
  const stateRef = useRef<GameState>('ready')
  const scoreRef = useRef(0)
  const requestRef = useRef<number | null>(null)
  const lastTimeRef = useRef(0)
  const birdRef = useRef<{ y: number; vy: number }>({ y: 0, vy: 0 })
  const pipesRef = useRef<Pipe[]>([])
  const snowRef = useRef<SnowFlake[]>([])

  useEffect(() => {
    stateRef.current = state
  }, [state])

  useEffect(() => {
    scoreRef.current = score
  }, [score])

  useEffect(() => {
    const resize = () => {
      const canvas = canvasRef.current
      if (!canvas) return
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
      if (stateRef.current === 'ready') {
        birdRef.current = { y: canvas.height * 0.5, vy: 0 }
        pipesRef.current = []
      }
      initSnow(canvas.width, canvas.height)
      drawScene()
    }

    resize()
    window.addEventListener('resize', resize)

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.code === 'Space' || event.code === 'ArrowUp') {
        event.preventDefault()
        handleInput()
      }
      if (event.code === 'KeyR' && stateRef.current === 'over') {
        event.preventDefault()
        startGame()
      }
    }

    window.addEventListener('keydown', onKeyDown)

    return () => {
      window.removeEventListener('resize', resize)
      window.removeEventListener('keydown', onKeyDown)
      stopLoop()
    }
  }, [])

  const stopLoop = () => {
    if (requestRef.current) {
      cancelAnimationFrame(requestRef.current)
      requestRef.current = null
    }
  }

  const handleInput = () => {
    if (stateRef.current === 'ready') {
      startGame()
      return
    }
    if (stateRef.current === 'playing') {
      birdRef.current.vy = FLAP_STRENGTH
      return
    }
    if (stateRef.current === 'over') {
      startGame()
    }
  }

  const startGame = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    birdRef.current = { y: canvas.height * 0.5, vy: 0 }
    pipesRef.current = []
    setScore(0)
    scoreRef.current = 0
    setState('playing')
    stateRef.current = 'playing'

    spawnPipe()
    lastTimeRef.current = performance.now()
    stopLoop()
    requestRef.current = requestAnimationFrame(tick)
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
    updateSnow(dt, width, height)
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
          scoreRef.current = next
          return next
        })
      }
    })

    while (pipes.length && pipes[0].x + pipeWidth < 0) {
      pipes.shift()
    }

    const hitTopOrBottom = bird.y - birdRadius <= 0 || bird.y + birdRadius >= height
    if (hitTopOrBottom) {
      endGame(scoreRef.current)
      return
    }

    const hitPipe = pipes.some((pipe) => {
      const withinPipe = birdX + birdRadius > pipe.x && birdX - birdRadius < pipe.x + pipeWidth
      const inGap = bird.y - birdRadius > pipe.gapY && bird.y + birdRadius < pipe.gapY + gapHeight
      return withinPipe && !inGap
    })

    if (hitPipe) {
      endGame(scoreRef.current)
    }
  }

  const endGame = (finalScore: number) => {
    if (stateRef.current === 'over') return
    setState('over')
    stateRef.current = 'over'
    stopLoop()
    onSendScore(finalScore)
  }

  const spawnPipe = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const height = canvas.height
    const pipeWidth = Math.max(68, Math.min(90, canvas.width * 0.18))
    const gapHeight = Math.max(150, Math.min(220, height * 0.25))
    const margin = Math.max(60, height * 0.12)
    const maxGapStart = height - gapHeight - margin
    const gapY = margin + Math.random() * Math.max(10, maxGapStart - margin)

    pipesRef.current.push({
      x: canvas.width + pipeWidth,
      gapY,
      passed: false,
    })
  }

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

    drawMoon(ctx, width, height)
    pipes.forEach((pipe) => {
      drawFlappyPipe(ctx, pipe, pipeWidth, gapHeight, height)
    })

    drawFlappyBird(ctx, birdX, bird.y, birdRadius, bird.vy)
    drawFlappyGround(ctx, height)
    drawSnow(ctx, width)
  }

  const drawFlappyPipe = (
    ctx: CanvasRenderingContext2D,
    pipe: Pipe,
    width: number,
    gapHeight: number,
    canvasHeight: number,
  ) => {
    const stripeWidth = Math.max(10, Math.min(18, width * 0.25))
    drawCandyPipeSegment(ctx, pipe.x, 0, width, pipe.gapY, stripeWidth)

    const bottomHeight = canvasHeight - (pipe.gapY + gapHeight)
    drawCandyPipeSegment(ctx, pipe.x, pipe.gapY + gapHeight, width, bottomHeight, stripeWidth)
  }

  const drawCandyPipeSegment = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number,
    stripeWidth: number,
  ) => {
    ctx.save()
    ctx.translate(x, y)

    ctx.beginPath()
    ctx.rect(0, 0, width, height)
    ctx.clip()

    const base = ctx.createLinearGradient(0, 0, width, height)
    base.addColorStop(0, '#f8fafc')
    base.addColorStop(1, '#e2e8f0')
    ctx.fillStyle = base
    ctx.fillRect(0, 0, width, height)

    ctx.strokeStyle = '#f43f5e'
    ctx.lineWidth = stripeWidth
    ctx.beginPath()
    for (let offset = -height; offset < width + height; offset += stripeWidth * 2) {
      ctx.moveTo(offset, 0)
      ctx.lineTo(offset + height, height)
    }
    ctx.stroke()

    ctx.strokeStyle = '#b91c1c'
    ctx.lineWidth = 4
    ctx.strokeRect(0, 0, width, height)

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)'
    ctx.lineWidth = 6
    ctx.beginPath()
    ctx.moveTo(6, 6)
    ctx.lineTo(6, height - 6)
    ctx.stroke()

    ctx.restore()
  }

  const drawFlappyBird = (
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

    const hatBaseY = -radius * 0.65
    ctx.fillStyle = '#dc2626'
    ctx.beginPath()
    ctx.moveTo(-radius * 0.9, hatBaseY + radius * 0.2)
    ctx.lineTo(radius * 0.9, hatBaseY + radius * 0.15)
    ctx.lineTo(0, hatBaseY - radius * 1.05)
    ctx.closePath()
    ctx.fill()

    ctx.fillStyle = '#f8fafc'
    ctx.beginPath()
    ctx.ellipse(radius * 0.02, hatBaseY + radius * 0.2, radius * 0.95, radius * 0.22, 0, 0, Math.PI * 2)
    ctx.fill()

    ctx.beginPath()
    ctx.arc(radius * 0.05, hatBaseY - radius * 1.08, radius * 0.28, 0, Math.PI * 2)
    ctx.fill()

    ctx.restore()
  }

  const drawFlappyGround = (ctx: CanvasRenderingContext2D, canvasHeight: number) => {
    const groundHeight = Math.max(40, canvasHeight * 0.1)
    const y = canvasHeight - groundHeight

    const snowGrad = ctx.createLinearGradient(0, y, 0, canvasHeight)
    snowGrad.addColorStop(0, '#e0f2fe')
    snowGrad.addColorStop(1, '#cbd5e1')
    ctx.fillStyle = snowGrad
    ctx.fillRect(0, y, ctx.canvas.width, groundHeight)

    ctx.fillStyle = 'rgba(255, 255, 255, 0.75)'
    const bumpWidth = Math.max(30, canvasHeight * 0.08)
    for (let i = -bumpWidth; i < ctx.canvas.width + bumpWidth; i += bumpWidth * 0.9) {
      const bumpHeight = groundHeight * (0.35 + Math.random() * 0.2)
      ctx.beginPath()
      ctx.ellipse(i, y + groundHeight * 0.6, bumpWidth, bumpHeight, 0, 0, Math.PI * 2)
      ctx.fill()
    }

    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'
    for (let i = 0; i < 50; i++) {
      const sx = Math.random() * ctx.canvas.width
      const sy = y + Math.random() * groundHeight
      ctx.fillRect(sx, sy, 1.5, 1.5)
    }
  }

  const drawMoon = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    const moonRadius = Math.max(26, Math.min(42, width * 0.05))
    const x = width - moonRadius - 40
    const y = Math.max(moonRadius + 30, height * 0.12)

    const glow = ctx.createRadialGradient(x, y, moonRadius * 0.5, x, y, moonRadius * 2)
    glow.addColorStop(0, 'rgba(248, 250, 252, 0.35)')
    glow.addColorStop(1, 'rgba(248, 250, 252, 0)')
    ctx.fillStyle = glow
    ctx.beginPath()
    ctx.arc(x, y, moonRadius * 2, 0, Math.PI * 2)
    ctx.fill()

    const moonGrad = ctx.createRadialGradient(
      x - moonRadius * 0.25,
      y - moonRadius * 0.2,
      moonRadius * 0.3,
      x,
      y,
      moonRadius,
    )
    moonGrad.addColorStop(0, '#f8fafc')
    moonGrad.addColorStop(1, '#e2e8f0')
    ctx.fillStyle = moonGrad
    ctx.beginPath()
    ctx.arc(x, y, moonRadius, 0, Math.PI * 2)
    ctx.fill()

    const craters = [
      { dx: -0.3, dy: -0.15, r: 0.22 },
      { dx: 0.25, dy: 0.1, r: 0.18 },
      { dx: 0.05, dy: -0.3, r: 0.12 },
    ]
    ctx.fillStyle = 'rgba(148, 163, 184, 0.5)'
    craters.forEach(({ dx, dy, r }) => {
      ctx.beginPath()
      ctx.arc(x + moonRadius * dx, y + moonRadius * dy, moonRadius * r, 0, Math.PI * 2)
      ctx.fill()
    })

    ctx.globalCompositeOperation = 'destination-out'
    ctx.beginPath()
    ctx.arc(x + moonRadius * 0.45, y - moonRadius * 0.05, moonRadius * 0.9, 0, Math.PI * 2)
    ctx.fill()
    ctx.globalCompositeOperation = 'source-over'
  }

  const initSnow = (width: number, height: number) => {
    const count = Math.max(140, Math.floor((width * height) / 16000))
    snowRef.current = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: 1.2 + Math.random() * 1.5,
      speed: 0.6 + Math.random() * 1.6,
      sway: 0.3 + Math.random() * 0.7,
      phase: Math.random() * Math.PI * 2,
      opacity: 0.45 + Math.random() * 0.4,
      layer: Math.random() < 0.35 ? 2 : 1,
    }))
  }

  const updateSnow = (dt: number, width: number, height: number) => {
    const snow = snowRef.current
    if (!snow.length) {
      initSnow(width, height)
      return
    }

    snow.forEach((flake) => {
      flake.phase += 0.02 * dt
      flake.x += Math.cos(flake.phase) * flake.sway * flake.layer
      flake.y += (flake.speed + flake.layer * 0.7) * dt

      if (flake.y > height + 8) {
        flake.y = -8
        flake.x = Math.random() * width
      }
      if (flake.x < -12) flake.x = width + 12
      if (flake.x > width + 12) flake.x = -12
    })
  }

  const drawSnow = (ctx: CanvasRenderingContext2D, width: number) => {
    if (!snowRef.current.length) return
    ctx.save()
    ctx.shadowColor = 'rgba(255, 255, 255, 0.45)'
    ctx.shadowBlur = Math.min(10, Math.max(4, width * 0.003))
    snowRef.current.forEach((flake) => {
      ctx.globalAlpha = Math.min(1, flake.opacity + flake.layer * 0.15)
      ctx.fillStyle = '#f8fafc'
      ctx.beginPath()
      ctx.arc(flake.x, flake.y, flake.radius * (flake.layer * 0.6 + 0.9), 0, Math.PI * 2)
      ctx.fill()
    })
    ctx.restore()
  }

  return (
    <>
      <canvas ref={canvasRef} className="game-canvas" onPointerDown={handleInput} />
      <div className="hud">
        <div className="score-badge">Счёт: {score}</div>
        {state === 'ready' && <div className="message">Тапни или нажми пробел, чтобы взлететь</div>}
        {state === 'over' && <div className="message">Игра окончена. Тапни, чтобы начать заново</div>}
      </div>
    </>
  )
}

export default FlappyGame
