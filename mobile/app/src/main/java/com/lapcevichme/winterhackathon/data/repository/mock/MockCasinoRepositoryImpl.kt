package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.core.config.CasinoConfig
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
            random < CasinoConfig.CHANCE_LEGENDARY -> Prize(
                "1",
                "Dragon Lore",
                PrizeType.ITEM,
                0,
                "🐉",
                CasinoConfig.Colors.LEGENDARY
            )

            random < CasinoConfig.CHANCE_EPIC -> Prize(
                "2",
                "Варежки",
                PrizeType.ITEM,
                0,
                "🧤",
                CasinoConfig.Colors.EPIC
            )

            random < CasinoConfig.CHANCE_RARE -> Prize(
                "3",
                "Кэшбек 5",
                PrizeType.MONEY,
                5,
                "💰",
                CasinoConfig.Colors.RARE
            )

            else -> Prize("4",
                "Стикер",
                PrizeType.TRASH,
                0,
                "💩",
                CasinoConfig.Colors.COMMON)
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