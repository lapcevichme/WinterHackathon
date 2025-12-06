package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.remote.GameApiService
import com.lapcevichme.winterhackathon.data.remote.GameScoreRequest
import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import javax.inject.Inject

class GameRepositoryImpl @Inject constructor(
    private val api: GameApiService
) : GameRepository {

    override suspend fun startGame(gameId: String): String {
        val response = api.startGame(gameId)
        return response.sessionId
    }

    override suspend fun sendScore(sessionId: String, score: Int) {
        val request = GameScoreRequest(
            sessionId = sessionId,
            score = score
        )
        api.sendScore(request)
    }
}