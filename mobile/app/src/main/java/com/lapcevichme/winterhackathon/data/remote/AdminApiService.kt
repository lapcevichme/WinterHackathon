package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface AdminApiService {
    @POST("admin/prizes/redeem")
    suspend fun redeemPrize(@Body request: AdminRedeemRequest): Response<AdminRedeemResponse>
}

@Serializable
data class AdminRedeemRequest(
    @SerialName("redeem_token")
    val redeemToken: String
)

@Serializable
data class AdminRedeemResponse(
    @SerialName("success")
    val success: Boolean,
    @SerialName("item_name")
    val itemName: String,
    @SerialName("user_display_name")
    val userDisplayName: String?,
    @SerialName("redeemed_at")
    val redeemedAt: String
)