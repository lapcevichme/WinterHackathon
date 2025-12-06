package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import okhttp3.MultipartBody
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Part
import retrofit2.http.Path

interface ProfileApiService {
    @GET("profile/me")
    suspend fun getMyProfile(): UserProfileDto
    @PATCH("profile/me")
    suspend fun updateProfile(@Body body: ProfilePatchDto): UserProfileDto
    @Multipart
    @PUT("users/me/picture")
    suspend fun updateProfilePicture(@Part file: MultipartBody.Part): UserModelDto
    @POST("profile/inventory/{item_id}/code")
    suspend fun generateRedeemToken(@Path("item_id") itemId: String): RedeemTokenResponseDto
    @GET("profile/balance")
    suspend fun getBalance(): BalanceDto
}

@Serializable
data class UserProfileDto(
    @SerialName("id") val id: String,
    @SerialName("username") val username: String? = null,
    @SerialName("display_name") val displayName: String? = null,
    @SerialName("department") val department: String? = null,
    @SerialName("avatar_url") val avatarUrl: String? = null,
    @SerialName("level") val level: Int,
    @SerialName("xp") val xp: Int,
    @SerialName("max_xp") val maxXp: Int,
    @SerialName("inventory") val inventory: List<InventoryItemDto>
)

@Serializable
data class ProfilePatchDto(
    @SerialName("display_name") val displayName: String? = null,
    @SerialName("avatar_url") val avatarUrl: String? = null
)

@Serializable
data class UserModelDto(
    @SerialName("id") val id: String,
    @SerialName("email") val email: String,
    @SerialName("username") val username: String? = null,
    @SerialName("display_name") val displayName: String? = null,
    @SerialName("profile_pic_url") val profilePicUrl: String? = null
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
data class RedeemTokenResponseDto(
    @SerialName("redeem_token") val redeemToken: String,
    @SerialName("expires_in_seconds") val expiresInSeconds: Int
)

@Serializable
data class BalanceDto(
    @SerialName("amount") val amount: Int,
    @SerialName("currency_symbol") val currencySymbol: String
)