package com.lapcevichme.winterhackathon.data.mapper

import com.lapcevichme.winterhackathon.data.remote.BalanceResponse
import com.lapcevichme.winterhackathon.data.remote.PrizeDto
import com.lapcevichme.winterhackathon.data.remote.SpinResponseDto
import com.lapcevichme.winterhackathon.domain.model.casino.Balance
import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import com.lapcevichme.winterhackathon.domain.model.casino.PrizeType
import com.lapcevichme.winterhackathon.domain.model.casino.SpinResponse

fun SpinResponseDto.toDomain(): SpinResponse {
    return SpinResponse(
        winner = winner.toDomain(),
        newBalance = newBalance.toDomain()
    )
}

fun BalanceResponse.toDomain(): Balance {
    return Balance(
        amount = amount,
        currencySymbol = currencySymbol
    )
}

fun PrizeDto.toDomain(): Prize {
    return Prize(
        id = id,
        name = name,
        type = try {
            PrizeType.valueOf(type.uppercase())
        } catch (e: Exception) {
            PrizeType.TRASH
        },
        amount = amount,
        emoji = emoji,
        colorHex = colorHex
    )
}