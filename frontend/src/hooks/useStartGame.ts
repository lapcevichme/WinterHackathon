import { useMutation } from '@tanstack/react-query'
import { startGameSession, type StartGameResponse } from '../api/api'

export const useStartGame = () =>
  useMutation<StartGameResponse, Error>({
    mutationFn: startGameSession,
  })
