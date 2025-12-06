const API_PREFIX = '/api/v1'

type ApiError = Error & { status?: number }

export type StartGameResponse = {
  session_id: string
  energy_left: number
}

export type SubmitScorePayload = {
  session_id: string
  score: number
}

export type SubmitScoreResponse = {
  success: boolean
  team_score_added: number
  total_team_score: number
}

export type ExchangeRequest = {
  code: string
}

export type TokenPair = {
  access_token: string
  refresh_token: string | null
}

let accessToken: string | null = null

export const setAccessToken = (token: string | null) => {
  accessToken = token
}

const request = async <T>(path: string, options: RequestInit = {}): Promise<T> => {
  const headers = new Headers(options.headers || undefined)
  if (accessToken) {
    headers.set('Authorization', `Bearer ${accessToken}`)
  }
  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  const response = await fetch(`${API_PREFIX}${path}`, {
    ...options,
    headers,
    credentials: 'include',
  })

  if (!response.ok) {
    const message = await response.text()
    const error = new Error(
      `Request to ${path} failed with ${response.status}${message ? `: ${message}` : ''}`,
    ) as ApiError
    error.status = response.status
    throw error
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

export const startGameSession = async (): Promise<StartGameResponse> => {
  return request<StartGameResponse>('/game/start', { method: 'POST' })
}

export const submitGameScore = async (
  payload: SubmitScorePayload,
): Promise<SubmitScoreResponse> => {
  return request<SubmitScoreResponse>('/game/score', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export const exchangeLaunchCode = async (payload: ExchangeRequest): Promise<TokenPair> => {
  return request<TokenPair>('/auth/webview/exchange', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
