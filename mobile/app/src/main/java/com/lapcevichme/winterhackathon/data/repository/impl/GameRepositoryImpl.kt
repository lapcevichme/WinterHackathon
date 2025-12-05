package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.remote.GameApi
import com.lapcevichme.winterhackathon.data.remote.GameResultRequestDto
import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import javax.inject.Inject

class GameRepositoryImpl @Inject constructor(
    private val api: GameApi
) : GameRepository {

    override suspend fun sendScore(score: Int) {
        val session = api.startGame()

        val request = GameResultRequestDto(
            sessionId = session.sessionId,
            score = score,
            winnerId = 1
        )

        api.sendGameResult(request)
    }
}