package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path

interface ProfileApiService {
    @GET("profile/me")
    suspend fun getMyProfile(): UserProfileDto

    @PATCH("profile/me")
    suspend fun updateProfile(@Body request: UpdateProfileRequest): UserProfileDto

    @POST("profile/inventory/{id}/code")
    suspend fun generateRedeemToken(@Path("id") inventoryId: String): RedeemTokenResponse

    @GET("profile/balance")
    suspend fun getBalance(): BalanceDto
}

@Serializable
data class UserProfileDto(
    @SerialName("id") val id: String,
    @SerialName("username") val username: String,
    @SerialName("display_name") val displayName: String,
    @SerialName("department") val department: String,
    @SerialName("avatar_url") val avatarUrl: String? = null,
    @SerialName("level") val level: Int,
    @SerialName("xp") val xp: Int,
    @SerialName("max_xp") val maxXp: Int,
    @SerialName("inventory") val inventory: List<InventoryItemDto>
)

@Serializable
data class InventoryItemDto(
    @SerialName("id") val id: String,
    @SerialName("prize_id") val prizeId: String? = null,
    @SerialName("name") val name: String,
    @SerialName("type") val type: String,
    @SerialName("status") val status: String,
    @SerialName("amount") val amount: Int,
    @SerialName("emoji") val emoji: String,
    @SerialName("color_hex") val colorHex: String
)

@Serializable
data class UpdateProfileRequest(
    @SerialName("display_name") val displayName: String? = null,
    @SerialName("avatar_url") val avatarUrl: String? = null
)

@Serializable
data class RedeemTokenResponse(
    @SerialName("redeem_token") val redeemToken: String,
    @SerialName("expires_in_seconds") val expiresInSeconds: Long
)

@Serializable
data class BalanceDto(
    @SerialName("amount") val amount: Int,
    @SerialName("currency_symbol") val currencySymbol: String
)