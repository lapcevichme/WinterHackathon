import { useMutation } from '@tanstack/react-query'
import {
  submitGameScore,
  type SubmitScorePayload,
  type SubmitScoreResponse,
} from '../api/api'

export const useSubmitScore = () =>
  useMutation<SubmitScoreResponse, Error, SubmitScorePayload>({
    mutationFn: submitGameScore,
  })
