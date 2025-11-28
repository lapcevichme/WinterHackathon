package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import javax.inject.Inject

class SendScoreUseCase @Inject constructor(
    private val repository: GameRepository
) {
    suspend operator fun invoke(score: Int) {
        repository.sendScore(score)
    }
}