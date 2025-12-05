package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.core.config.CasinoConfig
import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import com.lapcevichme.winterhackathon.domain.model.casino.PrizeType
import com.lapcevichme.winterhackathon.domain.model.casino.SpinResult
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import javax.inject.Inject

class SpinRouletteUseCase @Inject constructor(
    private val repository: CasinoRepository
) {
    suspend operator fun invoke(bet: Int): Result<SpinResult> {
        return try {
            val response = repository.spin(bet)

            val items = generateVisualStrip(response.winner)

            Result.success(
                SpinResult(
                    itemsChain = items,
                    winningIndex = CasinoConfig.WINNING_INDEX,
                    winPrize = response.winner,
                    newBalance = response.newBalance.amount
                )
            )
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun generateVisualStrip(winner: Prize): List<Prize> {
        val items = MutableList(CasinoConfig.TOTAL_ITEMS_IN_STRIP) { generateRandomTrash() }
        items[CasinoConfig.WINNING_INDEX] = winner
        return items
    }

    private fun generateRandomTrash(): Prize {
        val r = (0..100).random()
        return when {
            r < CasinoConfig.CHANCE_LEGENDARY ->
                Prize(
                    "trash_leg",
                    "Легендарное",
                    PrizeType.ITEM,
                    0,
                    "🐉",
                    CasinoConfig.Colors.LEGENDARY
                )

            r < CasinoConfig.CHANCE_EPIC ->
                Prize("trash_epic",
                    "Эпик",
                    PrizeType.ITEM,
                    0,
                    "🧤",
                    CasinoConfig.Colors.EPIC)

            r < CasinoConfig.CHANCE_RARE ->
                Prize("trash_rare",
                    "Кэшбек",
                    PrizeType.MONEY,
                    5,
                    "💰",
                    CasinoConfig.Colors.RARE)

            else ->
                Prize(
                    "trash_common",
                    "Обычное",
                    PrizeType.TRASH,
                    0,
                    "💩",
                    CasinoConfig.Colors.COMMON
                )
        }
    }
}