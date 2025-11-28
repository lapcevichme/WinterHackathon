package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import javax.inject.Inject


class MockGameRepositoryImpl @Inject constructor() : GameRepository {
    override suspend fun sendScore(score: Int) {
        println("Score sent to backend: $score")
    }
}
