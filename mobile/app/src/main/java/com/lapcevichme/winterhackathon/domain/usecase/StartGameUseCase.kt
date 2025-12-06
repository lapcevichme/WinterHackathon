package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import javax.inject.Inject

class StartGameUseCase @Inject constructor(
    private val repository: GameRepository
) {
    suspend operator fun invoke(gameId: String): String {
        return repository.startGame(gameId)
    }
}
