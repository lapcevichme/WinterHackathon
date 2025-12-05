package com.lapcevichme.winterhackathon.domain.repository

import com.lapcevichme.winterhackathon.data.remote.UserModel

interface UserRepository {
    suspend fun getUserMe(): Result<UserModel>
}