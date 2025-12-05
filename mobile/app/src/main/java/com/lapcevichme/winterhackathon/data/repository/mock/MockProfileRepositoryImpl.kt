package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.core.config.CasinoConfig
import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import com.lapcevichme.winterhackathon.domain.model.casino.PrizeType
import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile
import com.lapcevichme.winterhackathon.domain.repository.ProfileRepository
import kotlinx.coroutines.delay
import java.util.UUID
import javax.inject.Inject

class MockProfileRepositoryImpl @Inject constructor() : ProfileRepository {
    private var localProfile = UserProfile(
        id = "user_123",
        username = "@evinnik",
        displayName = "Егор Винник",
        department = "IT Отдел",
        avatarUrl = "https://i.pravatar.cc/300?img=11",
        level = 5,
        xp = 75,
        maxXp = 100,
        inventory = listOf(
            Prize(
                id = "1",
                name = "Перчатки Стажера",
                type = PrizeType.ITEM,
                emoji = "🧤",
                colorHex = CasinoConfig.Colors.COMMON
            ),
            Prize(
                id = "2",
                name = "Легаси Код",
                type = PrizeType.TRASH,
                emoji = "💩",
                colorHex = CasinoConfig.Colors.COMMON
            ),
            Prize(
                id = "3",
                name = "Красный Дракон",
                type = PrizeType.ITEM,
                emoji = "🐉",
                colorHex = CasinoConfig.Colors.LEGENDARY
            ),
            Prize(
                id = "4",
                name = "Макбук Про",
                type = PrizeType.ITEM,
                emoji = "💻",
                colorHex = CasinoConfig.Colors.RARE
            ),
            Prize(
                id = "5",
                name = "Бесконечный Кофе",
                type = PrizeType.ITEM,
                emoji = "☕",
                colorHex = CasinoConfig.Colors.EPIC
            )
        )
    )

    override suspend fun getMyProfile(): UserProfile {
        delay(600)
        return localProfile
    }

    override suspend fun generateRedeemToken(itemId: String): String {
        delay(1500)
        return "GIFT-${itemId}-${UUID.randomUUID().toString().take(8).uppercase()}"
    }

    override suspend fun updateProfile(displayName: String?, avatarUrl: String?): UserProfile {
        delay(1000)
        localProfile = localProfile.copy(
            displayName = displayName ?: localProfile.displayName,
            avatarUrl = avatarUrl ?: localProfile.avatarUrl
        )
        return localProfile
    }

    override suspend fun getBalance(): Int {
        delay(300)
        return 1250
    }
}