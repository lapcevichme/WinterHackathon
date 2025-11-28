package com.lapcevichme.winterhackathon.domain.usecase

import com.lapcevichme.winterhackathon.domain.model.main.MainScreenData
import com.lapcevichme.winterhackathon.domain.repository.MainRepository
import javax.inject.Inject

class GetMainScreenDataUseCase @Inject constructor(
    private val repository: MainRepository
) {
    suspend operator fun invoke(): MainScreenData {
        return repository.getMainScreenData()
    }
}