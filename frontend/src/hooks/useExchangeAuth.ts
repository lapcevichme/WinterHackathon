import { useMutation } from '@tanstack/react-query'
import { exchangeLaunchCode, type ExchangeRequest, type TokenPair } from '../api/api'

export const useExchangeAuth = () =>
  useMutation<TokenPair, Error, ExchangeRequest>({
    mutationFn: exchangeLaunchCode,
  })
