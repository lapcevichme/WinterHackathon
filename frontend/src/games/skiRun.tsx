import type { PointerEvent } from 'react'
import { useEffect, useRef, useState } from 'react'

type GameState = 'ready' | 'playing' | 'over'

type SkiSegment = {
  y: number
  center: number
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

type SkiRunProps = {
  onSendScore: (score: number) => void
}

const SKI_DIRECTION = {
  LEFT: -1,
  RIGHT: 1,
} as const

const getSkiParams = (width: number, height: number) => {
  const isMobile = width < 768
  const segmentLength = Math.max(isMobile ? 80 : 140, height * (isMobile ? 0.1 : 0.08))
  const segmentBuffer = segmentLength * 1.8
  const trackHalfWidth = Math.max(isMobile ? 60 : 70, width * (isMobile ? 0.22 : 0.18))
  const margin = Math.max(isMobile ? 36 : 48, width * (isMobile ? 0.12 : 0.1))
  const deltaXRange = Math.max(isMobile ? width * 0.22 : width * 0.12, isMobile ? 60 : 40)
  const verticalSpeed = isMobile ? 4.9 : 4.4
  const horizontalSpeed = isMobile ? 5 : 4.2
  const skierYFactor = isMobile ? 0.32 : 0.35
  return {
    segmentLength,
    segmentBuffer,
    trackHalfWidth,
    margin,
    deltaXRange,
    verticalSpeed,
    horizontalSpeed,
    skierYFactor,
  }
}

function SkiRunGame({ onSendScore }: SkiRunProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [state, setState] = useState<GameState>('ready')
  const [score, setScore] = useState(0)
  const stateRef = useRef<GameState>('ready')
  const scoreRef = useRef(0)
  const requestRef = useRef<number | null>(null)
  const lastTimeRef = useRef(0)
  const segmentsRef = useRef<SkiSegment[]>([])
  const skierRef = useRef<{ x: number; direction: -1 | 1 }>({
    x: 0,
    direction: SKI_DIRECTION.RIGHT,
  })
  const distanceRef = useRef(0)
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
        initSegments(canvas.width, canvas.height)
        skierRef.current = { x: canvas.width * 0.5, direction: SKI_DIRECTION.RIGHT }
        distanceRef.current = 0
      }
      initSnow(canvas.width, canvas.height)
      drawScene()
    }

    resize()
    window.addEventListener('resize', resize)

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.code === 'ArrowLeft') {
        event.preventDefault()
        handleInput('left')
      }
      if (event.code === 'ArrowRight') {
        event.preventDefault()
        handleInput('right')
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

  const handleInput = (side: 'left' | 'right') => {
    const currentState = stateRef.current
    if (currentState === 'ready' || currentState === 'over') {
      startGame(side)
      return
    }
    if (currentState !== 'playing') return
    skierRef.current.direction = side === 'left' ? SKI_DIRECTION.LEFT : SKI_DIRECTION.RIGHT
  }

  const startGame = (firstSide: 'left' | 'right') => {
    const canvas = canvasRef.current
    if (!canvas) return

    initSegments(canvas.width, canvas.height)
    skierRef.current = {
      x: canvas.width * 0.5,
      direction: firstSide === 'left' ? SKI_DIRECTION.LEFT : SKI_DIRECTION.RIGHT,
    }
    distanceRef.current = 0
    setScore(0)
    scoreRef.current = 0
    setState('playing')
    stateRef.current = 'playing'
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
    const params = getSkiParams(width, height)
    const dt = delta / (1000 / 60)
    updateSnow(dt, width, height)

    const speed = params.verticalSpeed * dt
    segmentsRef.current.forEach((seg) => {
      seg.y -= speed
    })

    while (
      segmentsRef.current.length > 2 &&
      segmentsRef.current[1].y < -params.segmentBuffer
    ) {
      segmentsRef.current.shift()
    }

    ensureSegments(width, height, params)

    const skier = skierRef.current
    skier.x += params.horizontalSpeed * dt * skier.direction
    skier.x = Math.max(20, Math.min(width - 20, skier.x))

    distanceRef.current += speed
    const nextScore = Math.floor(distanceRef.current / 6)
    if (nextScore !== scoreRef.current) {
      scoreRef.current = nextScore
      setScore(nextScore)
    }

    const skierY = height * params.skierYFactor
    const center = getCenterAt(skierY)
    const leftEdge = center - params.trackHalfWidth
    const rightEdge = center + params.trackHalfWidth
    if (skier.x < leftEdge + params.margin * 0.25 || skier.x > rightEdge - params.margin * 0.25) {
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

  const initSegments = (width: number, height: number) => {
    const params = getSkiParams(width, height)
    const segments: SkiSegment[] = []
    const startCenter = width * 0.5
    for (let y = 0; y <= height + params.segmentBuffer; y += params.segmentLength) {
      segments.push({ y, center: startCenter })
    }
    segmentsRef.current = segments
  }

  const ensureSegments = (width: number, height: number, params: ReturnType<typeof getSkiParams>) => {
    const segments = segmentsRef.current
    if (!segments.length) {
      initSegments(width, height)
      return
    }
    const margin = Math.max(params.margin, width * 0.1)

    while (segments[segments.length - 1].y < height + params.segmentBuffer) {
      const last = segments[segments.length - 1]
      const prev = segments[segments.length - 2] ?? last
      const trend = (last.center - prev.center) * 0.6
      const swing = (Math.random() * 2 - 1) * params.deltaXRange
      const nextCenter = clamp(last.center + trend + swing, margin, width - margin)
      segments.push({
        y: last.y + params.segmentLength,
        center: nextCenter,
      })
    }
  }

  const getCenterAt = (targetY: number) => {
    const segments = segmentsRef.current
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

  const drawScene = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const { width, height } = canvas
    const params = getSkiParams(width, height)
    const skierY = height * params.skierYFactor

    ctx.fillStyle = '#0b1f36'
    ctx.fillRect(0, 0, width, height)

    const segments = segmentsRef.current
    for (let i = 0; i < segments.length - 1; i++) {
      const a = segments[i]
      const b = segments[i + 1]
      ctx.beginPath()
      ctx.moveTo(a.center - params.trackHalfWidth, a.y)
      ctx.lineTo(a.center + params.trackHalfWidth, a.y)
      ctx.lineTo(b.center + params.trackHalfWidth, b.y)
      ctx.lineTo(b.center - params.trackHalfWidth, b.y)
      ctx.closePath()
      ctx.fillStyle = '#1e293b'
      ctx.fill()
      ctx.strokeStyle = '#94a3b8'
      ctx.lineWidth = 2
      ctx.stroke()
    }

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

    drawSnow(ctx, width)
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
      <canvas
        ref={canvasRef}
        className="game-canvas"
        onPointerDown={(event: PointerEvent<HTMLCanvasElement>) => {
          const canvas = canvasRef.current
          if (!canvas) return
          const side = event.clientX < canvas.getBoundingClientRect().width / 2 ? 'left' : 'right'
          handleInput(side)
        }}
      />
      <div className="hud">
        <div className="score-badge">Счёт: {score}</div>
        {state === 'ready' && (
          <div className="message">
            Ski run — тапни левую/правую сторону, чтобы задать направление
          </div>
        )}
        {state === 'over' && <div className="message">Столкновение. Тапни, чтобы начать снова</div>}
      </div>
    </>
  )
}

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value))

export default SkiRunGame
