package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.model.Prize
import com.lapcevichme.winterhackathon.domain.model.PrizeType
import com.lapcevichme.winterhackathon.domain.model.SpinResult
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository

class SpinRouletteUseCase(private val repository: CasinoRepository) {
    private val TOTAL_ITEMS = 50
    private val WINNING_INDEX = 40

    suspend operator fun invoke(bet: Int): Result<SpinResult> {
        return try {
            val response = repository.spin(bet)

            val items = generateVisualStrip(response.winner)

            Result.success(
                SpinResult(
                    itemsChain = items,
                    winningIndex = WINNING_INDEX,
                    winPrize = response.winner,
                    newBalance = response.newBalance
                )
            )
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun generateVisualStrip(winner: Prize): List<Prize> {
        val items = MutableList(TOTAL_ITEMS) { generateRandomTrash() }
        items[WINNING_INDEX] = winner
        return items
    }

    private fun generateRandomTrash(): Prize {
        val r = (0..100).random()
        return when {
            r < 5 -> Prize("trash", "Редкое", PrizeType.ITEM, 0, "⭐", 0xFFE91E63)
            r < 30 -> Prize("trash", "Кэшбек", PrizeType.MONEY, 5, "💰", 0xFF2196F3)
            else -> Prize("trash", "Мусор", PrizeType.TRASH, 0, "💩", 0xFF9E9E9E)
        }
    }
}