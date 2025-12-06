package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import javax.inject.Inject

class LaunchGameUseCase @Inject constructor(
    private val repository: GameRepository
) {
    suspend operator fun invoke(gameId: String): String {
        return repository.launchGame(gameId)
    }
}
