package com.lapcevichme.winterhackathon.domain.repository

interface GameRepository {
    suspend fun startGame(gameId: String): String
    suspend fun sendScore(sessionId: String, score: Int)
}