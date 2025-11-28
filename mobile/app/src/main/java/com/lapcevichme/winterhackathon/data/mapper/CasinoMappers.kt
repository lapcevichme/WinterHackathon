package com.lapcevichme.winterhackathon.data.mapper

import com.lapcevichme.winterhackathon.data.remote.PrizeDto
import com.lapcevichme.winterhackathon.data.remote.SpinResponseDto
import com.lapcevichme.winterhackathon.domain.model.casino.Prize
import com.lapcevichme.winterhackathon.domain.model.casino.PrizeType
import com.lapcevichme.winterhackathon.domain.model.casino.SpinResponse

fun PrizeDto.toDomain(): Prize {
    return Prize(
        id = this.id,
        name = this.name,
        type = try { PrizeType.valueOf(this.type) } catch (e: Exception) { PrizeType.TRASH },
        amount = this.amount,
        emoji = this.emoji,
        colorHex = this.colorHex
    )
}

fun SpinResponseDto.toDomain(): SpinResponse {
    return SpinResponse(
        winner = this.winner.toDomain(),
        newBalance = this.newBalance
    )
}