package com.lapcevichme.winterhackathon.domain.repository

interface GameRepository {
    suspend fun sendScore(score: Int)
}