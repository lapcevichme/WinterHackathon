import type { PointerEvent } from 'react'
import { useEffect, useRef, useState } from 'react'

type GameState = 'ready' | 'playing' | 'over'

type OsuTarget = {
  id: number
  x: number
  y: number
  radius: number
  born: number
  lifespan: number
  kind: 'gift' | 'coal'
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

type OsuProps = {
  onSendScore: (score: number) => void
}

const OSU_LIFESPAN = 1600
const OSU_SPAWN_INTERVAL_BASE = 900
const COAL_CHANCE = 0.10

function OsuGame({ onSendScore }: OsuProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [state, setState] = useState<GameState>('ready')
  const [score, setScore] = useState(0)
  const stateRef = useRef<GameState>('ready')
  const scoreRef = useRef(0)
  const requestRef = useRef<number | null>(null)
  const lastTimeRef = useRef(0)
  const lastSpawnRef = useRef(0)
  const targetsRef = useRef<OsuTarget[]>([])
  const nextIdRef = useRef(1)
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
        targetsRef.current = []
      }
      initSnow(canvas.width, canvas.height)
      drawScene()
    }

    resize()
    window.addEventListener('resize', resize)

    return () => {
      window.removeEventListener('resize', resize)
      stopLoop()
    }
  }, [])

  const stopLoop = () => {
    if (requestRef.current) {
      cancelAnimationFrame(requestRef.current)
      requestRef.current = null
    }
  }

  const handleTap = (event: PointerEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return

    const currentState = stateRef.current
    if (currentState === 'ready' || currentState === 'over') {
      startGame()
      return
    }
    if (currentState !== 'playing') return

    const rect = canvas.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * canvas.width
    const y = ((event.clientY - rect.top) / rect.height) * canvas.height

    const targets = targetsRef.current
    const hitIndex = targets.findIndex((target) => {
      const dx = x - target.x
      const dy = y - target.y
      return Math.sqrt(dx * dx + dy * dy) <= target.radius
    })

    if (hitIndex >= 0) {
      const hit = targets.splice(hitIndex, 1)[0]
      if (hit.kind === 'gift') {
        setScore((prev) => {
          const next = prev + 1
          scoreRef.current = next
          return next
        })
      } else {
        setScore((prev) => {
          const next = prev - 5
          scoreRef.current = next
          if (next <= 0) {
            endGame(next)
          }
          return next
        })
        if (scoreRef.current <= 0) {
          return
        }
      }
    }
  }

  const startGame = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    targetsRef.current = []
    nextIdRef.current = 1
    setScore(0)
    scoreRef.current = 0
    setState('playing')
    stateRef.current = 'playing'

    const now = performance.now()
    lastTimeRef.current = now
    lastSpawnRef.current = now
    spawnTarget(now)

    stopLoop()
    requestRef.current = requestAnimationFrame(tick)
  }

  const tick = (timestamp: number) => {
    const delta = Math.min(timestamp - lastTimeRef.current, 32)
    lastTimeRef.current = timestamp

    update(timestamp, delta)
    drawScene()

    if (stateRef.current === 'playing') {
      requestRef.current = requestAnimationFrame(tick)
    }
  }

  const update = (timestamp: number, delta: number) => {
    const canvas = canvasRef.current
    if (canvas) {
      const dt = delta / (1000 / 60)
      updateSnow(dt, canvas.width, canvas.height)
    }

    const targets = targetsRef.current

    if (!targets.length || timestamp - lastSpawnRef.current > getSpawnInterval()) {
      spawnTarget(timestamp)
    }

    const remaining: OsuTarget[] = []
    let giftExpired = false
    targets.forEach((target) => {
      if (timestamp - target.born > target.lifespan) {
        if (target.kind === 'gift') {
          giftExpired = true
        }
      } else {
        remaining.push(target)
      }
    })
    targetsRef.current = remaining
    if (giftExpired) endGame(scoreRef.current)
  }

  const endGame = (finalScore: number) => {
    if (stateRef.current === 'over') return
    setState('over')
    stateRef.current = 'over'
    stopLoop()
    onSendScore(finalScore)
  }

  const spawnTarget = (timestamp?: number) => {
    const canvas = canvasRef.current
    if (!canvas) return
    const now = timestamp ?? performance.now()
    const baseRadius = Math.max(28, Math.min(44, canvas.width * 0.05))
    const paddingX = Math.max(baseRadius + 28, canvas.width * 0.1)
    const paddingY = Math.max(baseRadius + 140, canvas.height * 0.22)
    const x = paddingX + Math.random() * Math.max(10, canvas.width - paddingX * 2)
    const y = paddingY + Math.random() * Math.max(10, canvas.height - paddingY * 2)
    const lifespan = OSU_LIFESPAN
    const kind: 'gift' | 'coal' = Math.random() < COAL_CHANCE ? 'coal' : 'gift'

    targetsRef.current.push({
      id: nextIdRef.current++,
      x,
      y,
      radius: baseRadius,
      born: now,
      lifespan,
      kind,
    })
    lastSpawnRef.current = now
  }

  const getSpawnInterval = () => {
    const tiers = Math.floor(scoreRef.current / 10)
    const reduction = Math.min(0.5, tiers * 0.06)
    return OSU_SPAWN_INTERVAL_BASE * (1 - reduction)
  }

  const drawScene = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const now = performance.now()
    ctx.fillStyle = '#081a2f'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    const targets = targetsRef.current
    targets.forEach((target) => {
      const age = now - target.born
      const lifeRatio = Math.max(0, 1 - age / target.lifespan)
      const pulse = 0.08 * Math.sin((age / target.lifespan) * Math.PI * 2)
      const radius = target.radius * (0.95 + pulse)

      ctx.save()
      ctx.translate(target.x, target.y)

      const accent = target.kind === 'gift' ? 'rgba(103, 232, 249, 0.6)' : 'rgba(148, 163, 184, 0.65)'
      ctx.strokeStyle = accent
      ctx.lineWidth = 6
      const approachRadius = radius + 18 * lifeRatio
      ctx.beginPath()
      ctx.arc(0, 0, approachRadius, 0, Math.PI * 2)
      ctx.stroke()

      const bodyGradient = ctx.createRadialGradient(
        -radius * 0.2,
        -radius * 0.2,
        radius * 0.15,
        0,
        0,
        radius,
      )
      if (target.kind === 'gift') {
        bodyGradient.addColorStop(0, '#38bdf8')
        bodyGradient.addColorStop(1, '#2563eb')
      } else {
        bodyGradient.addColorStop(0, '#cbd5e1')
        bodyGradient.addColorStop(1, '#475569')
      }
      ctx.fillStyle = bodyGradient
      ctx.beginPath()
      ctx.arc(0, 0, radius, 0, Math.PI * 2)
      ctx.fill()

      if (target.kind === 'gift') {
        ctx.strokeStyle = '#facc15'
        ctx.lineWidth = 5
        ctx.beginPath()
        ctx.arc(0, 0, radius * 0.8, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * lifeRatio)
        ctx.stroke()
        drawGift(ctx, radius * 0.9)
      } else {
        drawCoal(ctx, radius * 0.7, lifeRatio)
      }

      ctx.restore()
    })

    drawSnow(ctx, canvas.width)
  }

  const drawGift = (ctx: CanvasRenderingContext2D, size: number) => {
    const boxSize = size * 0.8
    const half = boxSize / 2
    const lidHeight = boxSize * 0.18
    const ribbonWidth = Math.max(3, boxSize * 0.08)

    ctx.fillStyle = '#ef4444'
    ctx.fillRect(-half, -half, boxSize, boxSize)

    ctx.fillStyle = '#dc2626'
    ctx.fillRect(-half, -half, boxSize, lidHeight)

    ctx.fillStyle = '#f59e0b'
    ctx.fillRect(-ribbonWidth / 2, -half, ribbonWidth, boxSize)
    ctx.fillRect(-half, -ribbonWidth / 2, boxSize, ribbonWidth)

    const bowWidth = boxSize * 0.32
    const bowHeight = boxSize * 0.2
    const bowY = -half + lidHeight * 0.4
    ctx.fillStyle = '#fde68a'
    ctx.beginPath()
    ctx.moveTo(-bowWidth * 0.1, bowY)
    ctx.quadraticCurveTo(-bowWidth * 0.7, bowY - bowHeight, 0, bowY - bowHeight * 0.9)
    ctx.quadraticCurveTo(bowWidth * 0.7, bowY - bowHeight, bowWidth * 0.1, bowY)
    ctx.closePath()
    ctx.fill()

    ctx.fillStyle = '#fef9c3'
    ctx.beginPath()
    ctx.arc(0, bowY - bowHeight * 0.35, ribbonWidth, 0, Math.PI * 2)
    ctx.fill()
  }

  const drawCoal = (ctx: CanvasRenderingContext2D, size: number, lifeRatio: number) => {
    const base = size
    ctx.fillStyle = '#111827'
    ctx.beginPath()
    ctx.arc(0, 0, base, 0, Math.PI * 2)
    ctx.fill()

    ctx.fillStyle = '#1f2937'
    for (let i = 0; i < 4; i++) {
      const angle = (Math.PI / 2) * i + lifeRatio * 0.5
      const rx = Math.cos(angle) * base * 0.4
      const ry = Math.sin(angle) * base * 0.4
      ctx.beginPath()
      ctx.ellipse(rx, ry, base * 0.35, base * 0.22, angle, 0, Math.PI * 2)
      ctx.fill()
    }

    ctx.fillStyle = '#9ca3af'
    ctx.beginPath()
    ctx.arc(-base * 0.2, -base * 0.25, base * 0.15, 0, Math.PI * 2)
    ctx.fill()
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
      <canvas ref={canvasRef} className="game-canvas" onPointerDown={handleTap} />
      <div className="hud">
        <div className="score-badge">Счёт: {score}</div>
        {state === 'ready' && <div className="message">osu! lite — тапай по кругам, пока они не исчезли</div>}
        {state === 'over' && <div className="message">Промах. Тапни, чтобы начать снова</div>}
      </div>
    </>
  )
}

export default OsuGame
