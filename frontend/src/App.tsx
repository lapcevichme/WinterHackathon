import type { PointerEvent } from 'react'
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
type GameTab = 'flappy' | 'osu' | 'ski'

type Pipe = {
  x: number
  gapY: number
  passed: boolean
}

type OsuTarget = {
  id: number
  x: number
  y: number
  radius: number
  born: number
  lifespan: number
}

type SkiSegment = {
  y: number
  center: number
}

// Flappy Bird tuning
const GRAVITY = 0.45
const FLAP_STRENGTH = -7.5
const BASE_SPEED = 2.8

// osu!-lite tuning
const OSU_LIFESPAN = 1600
const OSU_SPAWN_INTERVAL = 900

// Ski tuning
const SKI_VERTICAL_SPEED = 4.4
const SKI_HORIZONTAL_SPEED = 4.2
const SKI_SEGMENT_LENGTH = 140
const SKI_SEGMENT_BUFFER = 220
const SKI_DIRECTION = {
  LEFT: -1,
  RIGHT: 1,
} as const

function App() {
  const [activeGame, setActiveGame] = useState<GameTab>('flappy')

  // Flappy Bird state
  const flappyCanvasRef = useRef<HTMLCanvasElement | null>(null)
  const [flappyState, setFlappyState] = useState<GameState>('ready')
  const [flappyScore, setFlappyScore] = useState(0)
  const flappyStateRef = useRef<GameState>('ready')
  const flappyScoreRef = useRef(0)
  const flappyRequestRef = useRef<number | null>(null)
  const flappyLastTimeRef = useRef<number>(0)
  const birdRef = useRef<{ y: number; vy: number }>({ y: 0, vy: 0 })
  const pipesRef = useRef<Pipe[]>([])

  // osu!-lite state
  const osuCanvasRef = useRef<HTMLCanvasElement | null>(null)
  const [osuState, setOsuState] = useState<GameState>('ready')
  const [osuScore, setOsuScore] = useState(0)
  const osuStateRef = useRef<GameState>('ready')
  const osuScoreRef = useRef(0)
  const osuRequestRef = useRef<number | null>(null)
  const osuLastTimeRef = useRef(0)
  const osuLastSpawnRef = useRef(0)
  const osuTargetsRef = useRef<OsuTarget[]>([])
  const osuNextIdRef = useRef(1)

  // Ski state
  const skiCanvasRef = useRef<HTMLCanvasElement | null>(null)
  const [skiState, setSkiState] = useState<GameState>('ready')
  const [skiScore, setSkiScore] = useState(0)
  const skiStateRef = useRef<GameState>('ready')
  const skiScoreRef = useRef(0)
  const skiRequestRef = useRef<number | null>(null)
  const skiLastTimeRef = useRef(0)
  const skiSegmentsRef = useRef<SkiSegment[]>([])
  const skierRef = useRef<{ x: number; direction: -1 | 1 }>({
    x: 0,
    direction: SKI_DIRECTION.RIGHT,
  })
  const skiDistanceRef = useRef(0)

  useEffect(() => {
    flappyStateRef.current = flappyState
  }, [flappyState])
  useEffect(() => {
    flappyScoreRef.current = flappyScore
  }, [flappyScore])
  useEffect(() => {
    osuStateRef.current = osuState
  }, [osuState])
  useEffect(() => {
    osuScoreRef.current = osuScore
  }, [osuScore])
  useEffect(() => {
    skiStateRef.current = skiState
  }, [skiState])
  useEffect(() => {
    skiScoreRef.current = skiScore
  }, [skiScore])

  useEffect(() => {
    const resize = () => {
      const width = window.innerWidth
      const height = window.innerHeight

      const flappyCanvas = flappyCanvasRef.current
      if (flappyCanvas) {
        flappyCanvas.width = width
        flappyCanvas.height = height
        if (flappyStateRef.current === 'ready') {
          birdRef.current = { y: height * 0.5, vy: 0 }
          pipesRef.current = []
        }
        drawFlappyScene()
      }

      const osuCanvas = osuCanvasRef.current
      if (osuCanvas) {
        osuCanvas.width = width
        osuCanvas.height = height
        if (osuStateRef.current === 'ready') {
          osuTargetsRef.current = []
        }
        drawOsuScene()
      }

      const skiCanvas = skiCanvasRef.current
      if (skiCanvas) {
        skiCanvas.width = width
        skiCanvas.height = height
        if (skiStateRef.current === 'ready') {
          initSkiSegments(width, height)
          skierRef.current = { x: width * 0.5, direction: SKI_DIRECTION.RIGHT }
          skiDistanceRef.current = 0
        }
        drawSkiScene()
      }
    }

    resize()
    window.addEventListener('resize', resize)

    const onKeyDown = (event: KeyboardEvent) => {
      const currentActive = activeGame
      const currentFlappyState = flappyStateRef.current

      if (currentActive === 'flappy') {
        if (event.code === 'Space' || event.code === 'ArrowUp') {
          event.preventDefault()
          handleFlappyInput()
        }
        if (event.code === 'KeyR' && currentFlappyState === 'over') {
          event.preventDefault()
          startFlappy()
        }
      }

      if (currentActive === 'ski') {
        if (event.code === 'ArrowLeft') {
          event.preventDefault()
          handleSkiInput('left')
        }
        if (event.code === 'ArrowRight') {
          event.preventDefault()
          handleSkiInput('right')
        }
      }
    }

    window.addEventListener('keydown', onKeyDown)

    return () => {
      window.removeEventListener('resize', resize)
      window.removeEventListener('keydown', onKeyDown)
      stopFlappyLoop()
      stopOsuLoop()
      stopSkiLoop()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    // When switching games, pause both loops and reset the selected one to ready.
    stopFlappyLoop()
    stopOsuLoop()
    stopSkiLoop()

    if (activeGame === 'flappy') {
      setFlappyState('ready')
      flappyStateRef.current = 'ready'
      setFlappyScore(0)
      flappyScoreRef.current = 0
      pipesRef.current = []
      const canvas = flappyCanvasRef.current
      if (canvas) birdRef.current = { y: canvas.height * 0.5, vy: 0 }
      drawFlappyScene()
    } else if (activeGame === 'osu') {
      setOsuState('ready')
      osuStateRef.current = 'ready'
      setOsuScore(0)
      osuScoreRef.current = 0
      osuTargetsRef.current = []
      drawOsuScene()
    } else {
      setSkiState('ready')
      skiStateRef.current = 'ready'
      setSkiScore(0)
      skiScoreRef.current = 0
      const canvas = skiCanvasRef.current
      if (canvas) {
        initSkiSegments(canvas.width, canvas.height)
        skierRef.current = { x: canvas.width * 0.5, direction: SKI_DIRECTION.RIGHT }
        skiDistanceRef.current = 0
      }
      drawSkiScene()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeGame])

  const stopFlappyLoop = () => {
    if (flappyRequestRef.current) {
      cancelAnimationFrame(flappyRequestRef.current)
      flappyRequestRef.current = null
    }
  }

  const stopOsuLoop = () => {
    if (osuRequestRef.current) {
      cancelAnimationFrame(osuRequestRef.current)
      osuRequestRef.current = null
    }
  }

  const stopSkiLoop = () => {
    if (skiRequestRef.current) {
      cancelAnimationFrame(skiRequestRef.current)
      skiRequestRef.current = null
    }
  }

  const sendScore = (finalScore: number) => {
    if (window.AndroidGame?.sendScore) {
      window.AndroidGame.sendScore(finalScore)
    } else {
      console.log('Android bridge not found. Score:', finalScore)
      alert(`Очки отправлены: ${finalScore}`)
    }
  }

  // --- Flappy Bird ---
  const handleFlappyInput = () => {
    if (flappyStateRef.current === 'ready') {
      startFlappy()
      return
    }
    if (flappyStateRef.current === 'playing') {
      birdRef.current.vy = FLAP_STRENGTH
      return
    }
    if (flappyStateRef.current === 'over') {
      startFlappy()
    }
  }

  const startFlappy = () => {
    const canvas = flappyCanvasRef.current
    if (!canvas) return

    const height = canvas.height
    birdRef.current = { y: height * 0.5, vy: 0 }
    pipesRef.current = []
    setFlappyScore(0)
    flappyScoreRef.current = 0
    setFlappyState('playing')
    flappyStateRef.current = 'playing'

    spawnPipe()
    flappyLastTimeRef.current = performance.now()
    stopFlappyLoop()
    flappyRequestRef.current = requestAnimationFrame(flapppyTick)
  }

  const flapppyTick = (timestamp: number) => {
    const delta = Math.min(timestamp - flappyLastTimeRef.current, 32)
    flappyLastTimeRef.current = timestamp

    updateFlappy(delta)
    drawFlappyScene()

    if (flappyStateRef.current === 'playing') {
      flappyRequestRef.current = requestAnimationFrame(flapppyTick)
    }
  }

  const updateFlappy = (delta: number) => {
    const canvas = flappyCanvasRef.current
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
        setFlappyScore((prev) => {
          const next = prev + 1
          flappyScoreRef.current = next
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
      endFlappy(flappyScoreRef.current)
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
      endFlappy(flappyScoreRef.current)
    }
  }

  const endFlappy = (finalScore: number) => {
    if (flappyStateRef.current === 'over') return
    setFlappyState('over')
    flappyStateRef.current = 'over'
    stopFlappyLoop()
    sendScore(finalScore)
  }

  const spawnPipe = () => {
    const canvas = flappyCanvasRef.current
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

  const drawFlappyScene = () => {
    const canvas = flappyCanvasRef.current
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
      drawFlappyPipe(ctx, pipe, pipeWidth, gapHeight, height)
    })

    drawFlappyBird(ctx, birdX, bird.y, birdRadius, bird.vy)
    drawFlappyGround(ctx, height)
  }

  const drawFlappyPipe = (
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

    ctx.restore()
  }

  const drawFlappyGround = (
    ctx: CanvasRenderingContext2D,
    canvasHeight: number,
  ) => {
    const groundHeight = Math.max(20, canvasHeight * 0.06)
    const y = canvasHeight - groundHeight
    const gradient = ctx.createLinearGradient(0, y, 0, canvasHeight)
    gradient.addColorStop(0, '#0f8e51')
    gradient.addColorStop(1, '#0c6b3e')
    ctx.fillStyle = gradient
    ctx.fillRect(0, y, ctx.canvas.width, groundHeight)
  }

  // --- osu!-lite ---
  const handleOsuTap = (event: PointerEvent<HTMLCanvasElement>) => {
    const canvas = osuCanvasRef.current
    if (!canvas) return

    const state = osuStateRef.current
    if (state === 'ready' || state === 'over') {
      startOsu()
      return
    }
    if (state !== 'playing') return

    const rect = canvas.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * canvas.width
    const y = ((event.clientY - rect.top) / rect.height) * canvas.height

    const targets = osuTargetsRef.current
    const hitIndex = targets.findIndex((target) => {
      const dx = x - target.x
      const dy = y - target.y
      return Math.sqrt(dx * dx + dy * dy) <= target.radius
    })

    if (hitIndex >= 0) {
      targets.splice(hitIndex, 1)
      setOsuScore((prev) => {
        const next = prev + 1
        osuScoreRef.current = next
        return next
      })
    }
  }

  const startOsu = () => {
    const canvas = osuCanvasRef.current
    if (!canvas) return

    osuTargetsRef.current = []
    osuNextIdRef.current = 1
    setOsuScore(0)
    osuScoreRef.current = 0
    setOsuState('playing')
    osuStateRef.current = 'playing'

    const now = performance.now()
    osuLastTimeRef.current = now
    osuLastSpawnRef.current = now
    spawnOsuTarget(now)

    stopOsuLoop()
    osuRequestRef.current = requestAnimationFrame(osuTick)
  }

  const osuTick = (timestamp: number) => {
    osuLastTimeRef.current = timestamp

    updateOsu(timestamp)
    drawOsuScene()

    if (osuStateRef.current === 'playing') {
      osuRequestRef.current = requestAnimationFrame(osuTick)
    }
  }

  const updateOsu = (timestamp: number) => {
    const targets = osuTargetsRef.current

    if (!targets.length || timestamp - osuLastSpawnRef.current > OSU_SPAWN_INTERVAL) {
      spawnOsuTarget(timestamp)
    }

    const expired = targets.find(
      (target) => timestamp - target.born > target.lifespan,
    )
    if (expired) {
      endOsu(osuScoreRef.current)
    }
  }

  const endOsu = (finalScore: number) => {
    if (osuStateRef.current === 'over') return
    setOsuState('over')
    osuStateRef.current = 'over'
    stopOsuLoop()
    sendScore(finalScore)
  }

  const spawnOsuTarget = (timestamp?: number) => {
    const canvas = osuCanvasRef.current
    if (!canvas) return
    const now = timestamp ?? performance.now()
    const baseRadius = Math.max(28, Math.min(44, canvas.width * 0.05))
    const padding = baseRadius + 18
    const x = padding + Math.random() * Math.max(10, canvas.width - padding * 2)
    const y =
      padding + Math.random() * Math.max(10, canvas.height - padding * 2)
    const lifespan = OSU_LIFESPAN

    osuTargetsRef.current.push({
      id: osuNextIdRef.current++,
      x,
      y,
      radius: baseRadius,
      born: now,
      lifespan,
    })
    osuLastSpawnRef.current = now
  }

  const drawOsuScene = () => {
    const canvas = osuCanvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const now = performance.now()
    ctx.fillStyle = '#081a2f'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    const targets = osuTargetsRef.current
    targets.forEach((target) => {
      const age = now - target.born
      const lifeRatio = Math.max(0, 1 - age / target.lifespan)
      const pulse = 0.08 * Math.sin((age / target.lifespan) * Math.PI * 2)
      const radius = target.radius * (0.95 + pulse)

      ctx.save()
      ctx.translate(target.x, target.y)

      // Approach circle
      ctx.strokeStyle = 'rgba(103, 232, 249, 0.6)'
      ctx.lineWidth = 6
      const approachRadius = radius + 18 * lifeRatio
      ctx.beginPath()
      ctx.arc(0, 0, approachRadius, 0, Math.PI * 2)
      ctx.stroke()

      // Body
      const bodyGradient = ctx.createRadialGradient(
        -radius * 0.2,
        -radius * 0.2,
        radius * 0.15,
        0,
        0,
        radius,
      )
      bodyGradient.addColorStop(0, '#38bdf8')
      bodyGradient.addColorStop(1, '#2563eb')
      ctx.fillStyle = bodyGradient
      ctx.beginPath()
      ctx.arc(0, 0, radius, 0, Math.PI * 2)
      ctx.fill()

      // Inner ring
      ctx.strokeStyle = '#e0f2fe'
      ctx.lineWidth = 4
      ctx.beginPath()
      ctx.arc(0, 0, radius * 0.55, 0, Math.PI * 2)
      ctx.stroke()

      // Timer arc
      ctx.strokeStyle = '#facc15'
      ctx.lineWidth = 5
      ctx.beginPath()
      ctx.arc(
        0,
        0,
        radius * 0.8,
        -Math.PI / 2,
        -Math.PI / 2 + Math.PI * 2 * lifeRatio,
      )
      ctx.stroke()

      ctx.restore()
    })
  }

  // --- Ski ---
  const handleSkiInput = (side: 'left' | 'right') => {
    const state = skiStateRef.current
    if (state === 'ready' || state === 'over') {
      startSki(side)
      return
    }
    if (state !== 'playing') return
    skierRef.current.direction = side === 'left' ? SKI_DIRECTION.LEFT : SKI_DIRECTION.RIGHT
  }

  const startSki = (firstSide: 'left' | 'right') => {
    const canvas = skiCanvasRef.current
    if (!canvas) return

    initSkiSegments(canvas.width, canvas.height)
    skierRef.current = {
      x: canvas.width * 0.5,
      direction: firstSide === 'left' ? SKI_DIRECTION.LEFT : SKI_DIRECTION.RIGHT,
    }
    skiDistanceRef.current = 0
    setSkiScore(0)
    skiScoreRef.current = 0
    setSkiState('playing')
    skiStateRef.current = 'playing'
    skiLastTimeRef.current = performance.now()

    stopSkiLoop()
    skiRequestRef.current = requestAnimationFrame(skiTick)
  }

  const skiTick = (timestamp: number) => {
    const delta = Math.min(timestamp - skiLastTimeRef.current, 32)
    skiLastTimeRef.current = timestamp

    updateSki(delta)
    drawSkiScene()

    if (skiStateRef.current === 'playing') {
      skiRequestRef.current = requestAnimationFrame(skiTick)
    }
  }

  const updateSki = (delta: number) => {
    const canvas = skiCanvasRef.current
    if (!canvas) return

    const width = canvas.width
    const height = canvas.height
    const dt = delta / (1000 / 60)
    const trackHalfWidth = Math.max(70, width * 0.18)
    const margin = Math.max(48, width * 0.1)
    const skierY = height * 0.35

    // Move track up (skier goes down)
    const speed = SKI_VERTICAL_SPEED * dt
    skiSegmentsRef.current.forEach((seg) => {
      seg.y -= speed
    })

    // Remove segments above view
    while (
      skiSegmentsRef.current.length > 2 &&
      skiSegmentsRef.current[1].y < -SKI_SEGMENT_BUFFER
    ) {
      skiSegmentsRef.current.shift()
    }

    // Add new segments at bottom
    ensureSkiSegments(width, height)

    // Move skier horizontally
    const skier = skierRef.current
    skier.x += SKI_HORIZONTAL_SPEED * dt * skier.direction
    skier.x = Math.max(20, Math.min(width - 20, skier.x))

    skiDistanceRef.current += speed
    const nextScore = Math.floor(skiDistanceRef.current / 6)
    if (nextScore !== skiScoreRef.current) {
      skiScoreRef.current = nextScore
      setSkiScore(nextScore)
    }

    // Collision check
    const center = getSkiCenterAt(skierY)
    const leftEdge = center - trackHalfWidth
    const rightEdge = center + trackHalfWidth
    if (skier.x < leftEdge + margin * 0.25 || skier.x > rightEdge - margin * 0.25) {
      endSki(skiScoreRef.current)
    }
  }

  const endSki = (finalScore: number) => {
    if (skiStateRef.current === 'over') return
    setSkiState('over')
    skiStateRef.current = 'over'
    stopSkiLoop()
    sendScore(finalScore)
  }

  const initSkiSegments = (width: number, height: number) => {
    const segments: SkiSegment[] = []
    const startCenter = width * 0.5
    for (let y = 0; y <= height + SKI_SEGMENT_BUFFER; y += SKI_SEGMENT_LENGTH) {
      segments.push({ y, center: startCenter })
    }
    skiSegmentsRef.current = segments
  }

  const ensureSkiSegments = (width: number, height: number) => {
    const segments = skiSegmentsRef.current
    if (!segments.length) {
      initSkiSegments(width, height)
      return
    }
    const margin = Math.max(60, width * 0.18)

    while (segments[segments.length - 1].y < height + SKI_SEGMENT_BUFFER) {
      const last = segments[segments.length - 1]
      const deltaX = (Math.random() * 2 - 1) * Math.max(40, width * 0.12)
      const nextCenter = clamp(last.center + deltaX, margin, width - margin)
      segments.push({
        y: last.y + SKI_SEGMENT_LENGTH,
        center: nextCenter,
      })
    }
  }

  const getSkiCenterAt = (targetY: number) => {
    const segments = skiSegmentsRef.current
    if (!segments.length) return 0
    for (let i = 0; i < segments.length - 1; i++) {
      const a = segments[i]
      const b = segments[i + 1]
      if (targetY >= a.y && targetY <= b.y) {
        const t = (targetY - a.y) / (b.y - a.y || 1)
        return a.center + (b.center - a.center) * t
      }
    }
    return segments[segments.length - 1].center
  }

  const drawSkiScene = () => {
    const canvas = skiCanvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const { width, height } = canvas
    const trackHalfWidth = Math.max(70, width * 0.18)
    const skierY = height * 0.35

    ctx.fillStyle = '#0b1f36'
    ctx.fillRect(0, 0, width, height)

    // Draw track
    const segments = skiSegmentsRef.current
    for (let i = 0; i < segments.length - 1; i++) {
      const a = segments[i]
      const b = segments[i + 1]
      ctx.beginPath()
      ctx.moveTo(a.center - trackHalfWidth, a.y)
      ctx.lineTo(a.center + trackHalfWidth, a.y)
      ctx.lineTo(b.center + trackHalfWidth, b.y)
      ctx.lineTo(b.center - trackHalfWidth, b.y)
      ctx.closePath()
      ctx.fillStyle = '#1e293b'
      ctx.fill()
      ctx.strokeStyle = '#94a3b8'
      ctx.lineWidth = 2
      ctx.stroke()
    }

    // Draw skier
    const skier = skierRef.current
    ctx.save()
    ctx.translate(skier.x, skierY)
    ctx.fillStyle = '#e11d48'
    ctx.beginPath()
    ctx.moveTo(0, -18)
    ctx.lineTo(14, 16)
    ctx.lineTo(-14, 16)
    ctx.closePath()
    ctx.fill()
    ctx.fillStyle = '#f8fafc'
    ctx.fillRect(-3, -10, 6, 10)
    ctx.fillStyle = '#0ea5e9'
    ctx.fillRect(-6, 4, 12, 4)
    ctx.restore()
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
        <canvas
          ref={flappyCanvasRef}
          className="game-canvas"
          style={{ display: activeGame === 'flappy' ? 'block' : 'none' }}
          onPointerDown={handleFlappyInput}
        />
        <canvas
          ref={osuCanvasRef}
          className="game-canvas"
          style={{ display: activeGame === 'osu' ? 'block' : 'none' }}
          onPointerDown={handleOsuTap}
        />
        <canvas
          ref={skiCanvasRef}
          className="game-canvas"
          style={{ display: activeGame === 'ski' ? 'block' : 'none' }}
          onPointerDown={(event) => {
            const canvas = skiCanvasRef.current
            if (!canvas) return
            const side = event.clientX < canvas.getBoundingClientRect().width / 2 ? 'left' : 'right'
            handleSkiInput(side)
          }}
        />
      </div>

      <div className="hud">
        {activeGame === 'flappy' && (
          <>
            <div className="score-badge">Счёт: {flappyScore}</div>
            {flappyState === 'ready' && (
              <div className="message">Тапни или нажми пробел, чтобы взлететь</div>
            )}
            {flappyState === 'over' && (
              <div className="message">Игра окончена. Тапни, чтобы начать заново</div>
            )}
          </>
        )}

        {activeGame === 'osu' && (
          <>
            <div className="score-badge">Счёт: {osuScore}</div>
            {osuState === 'ready' && (
              <div className="message">osu! lite — тапай по кругам, пока они не исчезли</div>
            )}
            {osuState === 'over' && (
              <div className="message">Промах. Тапни, чтобы начать снова</div>
            )}
          </>
        )}

        {activeGame === 'ski' && (
          <>
            <div className="score-badge">Счёт: {skiScore}</div>
            {skiState === 'ready' && (
              <div className="message">
                Ski run — тапни левую/правую сторону, чтобы задать направление
              </div>
            )}
            {skiState === 'over' && (
              <div className="message">Столкновение. Тапни, чтобы начать снова</div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

const clamp = (value: number, min: number, max: number) =>
  Math.min(max, Math.max(min, value))

export default App
