package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.domain.model.Prize
import com.lapcevichme.winterhackathon.domain.model.PrizeType
import com.lapcevichme.winterhackathon.domain.model.SpinResponse
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import kotlinx.coroutines.delay

class MockCasinoRepositoryImpl : CasinoRepository {
    private var localBalance = 100

    override suspend fun getUserBalance(): Int = localBalance

    override suspend fun spin(bet: Int): SpinResponse {
        delay(500)
        if (localBalance < bet) throw Exception("Деньги закончились... плаки")

        localBalance -= bet

        val random = (0..100).random()
        val winner = when {
            random < 2 -> Prize("1", "Dragon Lore", PrizeType.ITEM, 0, "🐉", 0xFFFFD700)
            random < 10 -> Prize("2", "Варежки", PrizeType.ITEM, 0, "🧤", 0xFFE91E63)
            random < 40 -> Prize("3", "Кэшбек 5", PrizeType.MONEY, 5, "💰", 0xFF2196F3)
            else -> Prize("4", "Стикер", PrizeType.TRASH, 0, "💩", 0xFF9E9E9E)
        }

        if (winner.type == PrizeType.MONEY) {
            localBalance += winner.amount
        }

        return SpinResponse(
            winner = winner,
            newBalance = localBalance
        )
    }
}