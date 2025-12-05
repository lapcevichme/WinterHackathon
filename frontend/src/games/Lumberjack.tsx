import type { PointerEvent } from 'react'
import { useEffect, useRef, useState } from 'react'

type GameState = 'ready' | 'playing' | 'over'
type Side = 'left' | 'right'

type Segment = {
  icicle: Side | 'none'
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

type LumberjackProps = {
  onSendScore: (score: number) => void
}

const SEGMENTS = 14
const START_TIME = 5600
const MAX_TIME = 8200
const BASE_BONUS = 1100

const getMaxTime = (score: number = 0) =>
  Math.max(1000, MAX_TIME - Math.floor(score / 10) * 1200)
const getStartTime = (score: number = 0) =>
  Math.max(1000, START_TIME - Math.floor(score / 10) * 760)

function LumberjackGame({ onSendScore }: LumberjackProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [state, setState] = useState<GameState>('ready')
  const [score, setScore] = useState(0)
  const stateRef = useRef<GameState>('ready')
  const scoreRef = useRef(0)
  const requestRef = useRef<number | null>(null)
  const lastTimeRef = useRef(0)
  const towerRef = useRef<Segment[]>([])
  const playerSideRef = useRef<Side>('left')
  const timeRef = useRef(START_TIME)
  const snowRef = useRef<SnowFlake[]>([])
  const hitFlashRef = useRef(0)
  const shakeRef = useRef(0)

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
      if (!towerRef.current.length || stateRef.current === 'ready') {
        initTower()
        timeRef.current = getStartTime(scoreRef.current)
      }
      initSnow(canvas.width, canvas.height)
      drawScene()
    }

    resize()
    window.addEventListener('resize', resize)

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.code === 'ArrowLeft' || event.code === 'KeyA') {
        event.preventDefault()
        handleInput('left')
      }
      if (event.code === 'ArrowRight' || event.code === 'KeyD') {
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

  const initTower = () => {
    const stack: Segment[] = []
    for (let i = 0; i < SEGMENTS; i++) {
      if (i < 3) {
        stack.push({ icicle: 'none' })
      } else {
        stack.push(createSegment())
      }
    }
    towerRef.current = stack
  }

  const createSegment = (): Segment => {
    const hazardChance = Math.min(0.68, 0.28 + scoreRef.current * 0.0065)
    const icicle =
      Math.random() < hazardChance ? (Math.random() < 0.5 ? 'left' : 'right') : 'none'
    return { icicle }
  }

  const handleTap = (event: PointerEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return
    const rect = canvas.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * canvas.width
    const side: Side = x < canvas.width / 2 ? 'left' : 'right'
    handleInput(side)
  }

  const handleInput = (side: Side) => {
    const current = stateRef.current
    if (current === 'ready' || current === 'over') {
      startGame(side)
      return
    }
    if (current !== 'playing') return
    chop(side)
  }

  const startGame = (side: Side) => {
    const canvas = canvasRef.current
    if (!canvas) return

    initTower()
    playerSideRef.current = side
    timeRef.current = getStartTime()
    setScore(0)
    scoreRef.current = 0
    setState('playing')
    stateRef.current = 'playing'
    lastTimeRef.current = performance.now()
    hitFlashRef.current = 0
    shakeRef.current = 0

    stopLoop()
    requestRef.current = requestAnimationFrame(tick)
  }

  const chop = (side: Side) => {
    playerSideRef.current = side
    hitFlashRef.current = 1
    shakeRef.current = 6

    const tower = towerRef.current
    const bottom = tower[0]
    if (bottom && bottom.icicle === side) {
      endGame(scoreRef.current)
      return
    }

    tower.shift()
    tower.push(createSegment())

    const gain = Math.max(360, BASE_BONUS - scoreRef.current * 6.5)
    const maxTime = getMaxTime(scoreRef.current)
    timeRef.current = Math.min(maxTime, timeRef.current + gain)

    setScore((prev) => {
      const next = prev + 1
      scoreRef.current = next
      return next
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
    const maxTime = getMaxTime(scoreRef.current)

    updateSnow(dt, width, height)

    const drain = delta * (1.35 + scoreRef.current * 0.004)
    timeRef.current = Math.min(timeRef.current, maxTime)
    timeRef.current -= drain
    if (timeRef.current <= 0) {
      endGame(scoreRef.current)
      return
    }

    if (shakeRef.current > 0) {
      shakeRef.current = Math.max(0, shakeRef.current - delta * 0.025)
    }
    if (hitFlashRef.current > 0) {
      hitFlashRef.current = Math.max(0, hitFlashRef.current - delta * 0.0035)
    }
  }

  const endGame = (finalScore: number) => {
    if (stateRef.current === 'over') return
    setState('over')
    stateRef.current = 'over'
    stopLoop()
    onSendScore(finalScore)
  }

  const drawScene = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const width = canvas.width
    const height = canvas.height
    const now = performance.now()
    const maxTime = getMaxTime(scoreRef.current)

    const bg = ctx.createLinearGradient(0, 0, 0, height)
    bg.addColorStop(0, '#0a1a2c')
    bg.addColorStop(1, '#0b355a')
    ctx.fillStyle = bg
    ctx.fillRect(0, 0, width, height)

    drawSnow(ctx, width)

    const towerWidth = Math.max(86, Math.min(130, width * 0.18))
    const segmentHeight = Math.max(38, Math.min(68, height * 0.065))
    const baseY = height - Math.max(120, height * 0.12)
    const towerX = width / 2

    ctx.fillStyle = '#0f172a'
    ctx.beginPath()
    ctx.ellipse(towerX, baseY + 38, towerWidth * 1.4, 28, 0, 0, Math.PI * 2)
    ctx.fill()

    const shake = stateRef.current === 'playing' ? shakeRef.current : 0
    const wobbleX = shake ? Math.sin(now * 0.08) * shake : 0
    const wobbleY = shake ? Math.cos(now * 0.12) * shake * 0.6 : 0
    ctx.save()
    ctx.translate(wobbleX, wobbleY)

    for (let i = 0; i < SEGMENTS; i++) {
      const seg = towerRef.current[i]
      const y = baseY - i * segmentHeight
      const lightness = 0.92 - i * 0.04 + hitFlashRef.current * 0.12
      const opacity = Math.max(0.32, 0.85 - i * 0.04)
      const bodyGradient = ctx.createLinearGradient(
        towerX - towerWidth / 2,
        y - segmentHeight,
        towerX + towerWidth / 2,
        y,
      )
      bodyGradient.addColorStop(0, `rgba(148, 214, 255, ${opacity})`)
      bodyGradient.addColorStop(1, `rgba(118, 187, 241, ${opacity})`)

      ctx.fillStyle = bodyGradient
      ctx.strokeStyle = `rgba(226, 241, 255, ${Math.max(0.15, opacity - 0.2)})`
      ctx.lineWidth = 3
      roundRect(
        ctx,
        towerX - towerWidth / 2,
        y - segmentHeight + 4,
        towerWidth,
        segmentHeight - 6,
        10,
      )
      ctx.fill()
      ctx.stroke()

      ctx.fillStyle = `rgba(226, 241, 255, ${Math.min(0.5, lightness)})`
      ctx.fillRect(towerX - towerWidth / 2 + 8, y - segmentHeight + 10, 8, segmentHeight - 20)

      if (seg && seg.icicle !== 'none') {
        const isLeft = seg.icicle === 'left'
        const icicleWidth = towerWidth * 0.42
        const spikeHeight = segmentHeight * 0.85
        ctx.fillStyle = 'rgba(125, 211, 252, 0.8)'
        ctx.strokeStyle = 'rgba(240, 249, 255, 0.8)'
        ctx.lineWidth = 2.5
        ctx.beginPath()
        if (isLeft) {
          ctx.moveTo(towerX - towerWidth / 2, y - segmentHeight + 4)
          ctx.lineTo(towerX - towerWidth / 2 - icicleWidth, y - segmentHeight + spikeHeight * 0.55)
          ctx.lineTo(towerX - towerWidth / 2, y + 2)
        } else {
          ctx.moveTo(towerX + towerWidth / 2, y - segmentHeight + 4)
          ctx.lineTo(towerX + towerWidth / 2 + icicleWidth, y - segmentHeight + spikeHeight * 0.55)
          ctx.lineTo(towerX + towerWidth / 2, y + 2)
        }
        ctx.closePath()
        ctx.fill()
        ctx.stroke()
      }
    }

    drawPlayer(ctx, towerX, baseY, towerWidth, segmentHeight)
    drawTimer(ctx, width, Math.max(0, timeRef.current) / maxTime)

    ctx.restore()
  }

  const drawPlayer = (
    ctx: CanvasRenderingContext2D,
    towerX: number,
    baseY: number,
    towerWidth: number,
    segmentHeight: number,
  ) => {
    const side = playerSideRef.current
    const direction = side === 'left' ? -1 : 1
    const px = towerX + direction * (towerWidth * 0.78)
    const py = baseY + segmentHeight * 0.08
    const swing = hitFlashRef.current * 0.45 * direction

    ctx.save()
    ctx.translate(px, py)
    ctx.rotate(swing)

    ctx.fillStyle = 'rgba(0, 0, 0, 0.35)'
    ctx.beginPath()
    ctx.ellipse(0, segmentHeight * 0.9, towerWidth * 0.32, 16, 0, 0, Math.PI * 2)
    ctx.fill()

    ctx.fillStyle = '#0ea5e9'
    ctx.strokeStyle = '#7dd3fc'
    ctx.lineWidth = 3
    roundRect(ctx, -towerWidth * 0.18, -segmentHeight * 0.2, towerWidth * 0.36, segmentHeight * 0.9, 10)
    ctx.fill()
    ctx.stroke()

    ctx.fillStyle = '#1f2937'
    roundRect(ctx, -towerWidth * 0.16, -segmentHeight * 0.45, towerWidth * 0.32, segmentHeight * 0.38, 8)
    ctx.fill()

    ctx.fillStyle = '#e2e8f0'
    ctx.beginPath()
    ctx.arc(0, -segmentHeight * 0.6, segmentHeight * 0.18, 0, Math.PI * 2)
    ctx.fill()

    ctx.fillStyle = '#ef4444'
    ctx.beginPath()
    ctx.moveTo(-towerWidth * 0.16, -segmentHeight * 0.7)
    ctx.lineTo(0, -segmentHeight * 0.9)
    ctx.lineTo(towerWidth * 0.16, -segmentHeight * 0.7)
    ctx.closePath()
    ctx.fill()

    ctx.strokeStyle = '#0f172a'
    ctx.lineWidth = 3
    ctx.beginPath()
    ctx.moveTo(-towerWidth * 0.08, -segmentHeight * 0.6)
    ctx.lineTo(-towerWidth * 0.02, -segmentHeight * 0.55)
    ctx.moveTo(towerWidth * 0.02, -segmentHeight * 0.55)
    ctx.lineTo(towerWidth * 0.08, -segmentHeight * 0.6)
    ctx.stroke()

    ctx.strokeStyle = '#e2e8f0'
    ctx.lineWidth = 4
    ctx.beginPath()
    ctx.moveTo(-towerWidth * 0.04, -segmentHeight * 0.45)
    ctx.lineTo(towerWidth * 0.04, -segmentHeight * 0.45)
    ctx.stroke()

    const axeX = towerWidth * 0.22 * direction
    ctx.save()
    ctx.translate(axeX, -segmentHeight * 0.2)
    ctx.rotate(direction * -0.45 + swing * 0.35)
    ctx.fillStyle = '#f8fafc'
    roundRect(ctx, -8, -segmentHeight * 0.32, 16, segmentHeight * 0.36, 4)
    ctx.fill()
    ctx.fillStyle = '#e5e7eb'
    ctx.fillRect(-3, -segmentHeight * 0.58, 6, segmentHeight * 0.38)
    ctx.restore()

    ctx.restore()
  }

  const drawTimer = (ctx: CanvasRenderingContext2D, width: number, ratio: number) => {
    const clamped = Math.max(0, Math.min(1, ratio))
    const barWidth = Math.min(420, width * 0.7)
    const barHeight = 16
    const x = width / 2 - barWidth / 2
    const y = 18

    ctx.save()
    ctx.globalAlpha = 0.92
    ctx.fillStyle = 'rgba(255, 255, 255, 0.1)'
    roundRect(ctx, x, y, barWidth, barHeight, 10)
    ctx.fill()

    const fill = ctx.createLinearGradient(x, y, x + barWidth, y)
    fill.addColorStop(0, '#22d3ee')
    fill.addColorStop(1, '#2563eb')
    ctx.fillStyle = fill
    roundRect(ctx, x + 2, y + 2, (barWidth - 4) * clamped, barHeight - 4, 8)
    ctx.fill()

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.22)'
    ctx.lineWidth = 2
    roundRect(ctx, x, y, barWidth, barHeight, 10)
    ctx.stroke()
    ctx.restore()
  }

  const roundRect = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
    r: number,
  ) => {
    ctx.beginPath()
    ctx.moveTo(x + r, y)
    ctx.lineTo(x + w - r, y)
    ctx.quadraticCurveTo(x + w, y, x + w, y + r)
    ctx.lineTo(x + w, y + h - r)
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
    ctx.lineTo(x + r, y + h)
    ctx.quadraticCurveTo(x, y + h, x, y + h - r)
    ctx.lineTo(x, y + r)
    ctx.quadraticCurveTo(x, y, x + r, y)
    ctx.closePath()
  }

  const initSnow = (width: number, height: number) => {
    const count = Math.max(120, Math.floor((width * height) / 18000))
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
      <canvas ref={canvasRef} className="game-canvas" onPointerDown={handleTap} />
      <div className="hud">
        <div className="score-badge">Счёт: {score}</div>
        {state === 'ready' && (
          <div className="message">Ice Lumberjack — тапай слева или справа, руби лёд и уходи от сосулек</div>
        )}
        {state === 'over' && (
          <div className="message">Сосулька задела или кончилось время. Тапни, чтобы начать снова</div>
        )}
      </div>
    </>
  )
}

export default LumberjackGame
