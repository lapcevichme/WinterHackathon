package com.lapcevichme.winterhackathon.data.repository.mock

import com.lapcevichme.winterhackathon.core.config.CasinoConfig
import com.lapcevichme.winterhackathon.domain.model.profile.InventoryItem
import com.lapcevichme.winterhackathon.domain.model.profile.ItemStatus
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
            InventoryItem(
                id = "1",
                prizeId = "1",
                name = "Перчатки Стажера",
                type = com.lapcevichme.winterhackathon.domain.model.casino.PrizeType.ITEM,
                status = ItemStatus.AVAILABLE,
                amount = 1,
                emoji = "🧤",
                colorHex = com.lapcevichme.winterhackathon.core.config.CasinoConfig.Colors.COMMON
            ),
            InventoryItem(
                id = "2",
                prizeId = "2",
                name = "Легаси Код",
                type = com.lapcevichme.winterhackathon.domain.model.casino.PrizeType.TRASH,
                status = ItemStatus.AVAILABLE,
                amount = 1,
                emoji = "💩",
                colorHex = com.lapcevichme.winterhackathon.core.config.CasinoConfig.Colors.COMMON
            ),
            InventoryItem(
                id = "3",
                prizeId = "3",
                name = "Красный Дракон",
                type = com.lapcevichme.winterhackathon.domain.model.casino.PrizeType.ITEM,
                status = ItemStatus.AVAILABLE,
                amount = 1,
                emoji = "🐉",
                colorHex = com.lapcevichme.winterhackathon.core.config.CasinoConfig.Colors.LEGENDARY
            ),
            InventoryItem(
                id = "4",
                prizeId = "4",
                name = "Макбук Про",
                type = com.lapcevichme.winterhackathon.domain.model.casino.PrizeType.ITEM,
                status = ItemStatus.AVAILABLE,
                amount = 1,
                emoji = "💻",
                colorHex = com.lapcevichme.winterhackathon.core.config.CasinoConfig.Colors.RARE
            ),
            InventoryItem(
                id = "5",
                prizeId = "5",
                name = "Бесконечный Кофе",
                type = com.lapcevichme.winterhackathon.domain.model.casino.PrizeType.ITEM,
                status = ItemStatus.AVAILABLE,
                amount = 1,
                emoji = "☕",
                colorHex = com.lapcevichme.winterhackathon.core.config.CasinoConfig.Colors.EPIC
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

    override suspend fun uploadAvatar(imageBytes: ByteArray): UserProfile {
        TODO("Not yet implemented")
    }

    override suspend fun getBalance(): Int {
        delay(300)
        return 1250
    }
}