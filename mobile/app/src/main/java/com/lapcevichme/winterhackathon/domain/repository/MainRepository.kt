package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.domain.model.main.MainScreenData

interface MainRepository {
    suspend fun getMainScreenData(): MainScreenData
}