package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile

interface ProfileRepository {
    suspend fun getMyProfile(): UserProfile
    suspend fun generateRedeemToken(itemId: String): String
}
