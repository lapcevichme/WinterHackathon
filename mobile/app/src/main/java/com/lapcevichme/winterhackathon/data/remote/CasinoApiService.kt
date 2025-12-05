package com.lapcevichme.winterhackathon.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface CasinoApiService {
    @GET("profile/balance")
    suspend fun getUserBalance(): BalanceResponse

    @POST("casino/spin")
    suspend fun spin(@Body request: SpinRequest): SpinResponseDto
}

@Serializable
data class BalanceResponse(
    @SerialName("amount")
    val amount: Int,
    @SerialName("currency_symbol")
    val currencySymbol: String
)

@Serializable
data class SpinRequest(
    @SerialName("bet")
    val bet: Int
)

@Serializable
data class SpinResponseDto(
    @SerialName("winner")
    val winner: PrizeDto,

    @SerialName("new_balance")
    val newBalance: BalanceResponse
)

@Serializable
data class PrizeDto(
    @SerialName("id")
    val id: String,

    @SerialName("name")
    val name: String,

    @SerialName("type")
    val type: String, // "ITEM", "MONEY", "TRASH"

    @SerialName("amount")
    val amount: Int,

    @SerialName("emoji")
    val emoji: String,

    @SerialName("color_hex")
    val colorHex: String
)