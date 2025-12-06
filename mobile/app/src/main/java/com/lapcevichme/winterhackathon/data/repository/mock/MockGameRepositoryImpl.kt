package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import javax.inject.Inject


class MockGameRepositoryImpl @Inject constructor() : GameRepository {

    override suspend fun startGame(gameId: String): String {
        return "mock-session-id"
    }

    override suspend fun launchGame(gameId: String): String {
        TODO("Not yet implemented")
    }

    override suspend fun sendScore(sessionId: String, score: Int) {
        // Do nothing
    }
}
