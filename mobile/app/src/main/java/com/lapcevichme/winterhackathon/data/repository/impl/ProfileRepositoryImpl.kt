package com.lapcevichme.winterhackathon.data.repository.impl

import com.lapcevichme.winterhackathon.data.mapper.toDomain
import com.lapcevichme.winterhackathon.data.remote.ProfileApiService
import com.lapcevichme.winterhackathon.data.remote.ProfilePatchDto
import com.lapcevichme.winterhackathon.domain.model.profile.UserProfile
import com.lapcevichme.winterhackathon.domain.repository.ProfileRepository
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import javax.inject.Inject

class ProfileRepositoryImpl @Inject constructor(
    private val api: ProfileApiService
) : ProfileRepository {

    override suspend fun getMyProfile(): UserProfile {
        return api.getMyProfile().toDomain()
    }

    override suspend fun generateRedeemToken(itemId: String): String {
        return api.generateRedeemToken(itemId).redeemToken
    }

    override suspend fun updateProfile(displayName: String?, avatarUrl: String?): UserProfile {
        val request = ProfilePatchDto(
            displayName = displayName,
            avatarUrl = avatarUrl
        )
        return api.updateProfile(request).toDomain()
    }

    override suspend fun uploadAvatar(imageBytes: ByteArray): UserProfile {
        val requestFile = imageBytes.toRequestBody("image/jpeg".toMediaTypeOrNull())
        val body = MultipartBody.Part.createFormData("file", "avatar.jpg", requestFile)

        api.updateProfilePicture(body)

        return api.getMyProfile().toDomain()
    }

    override suspend fun getBalance(): Int {
        return api.getBalance().amount
    }
}