package com.lapcevichme.winterhackathon.core.network

import com.lapcevichme.winterhackathon.core.manager.TokenManager
import com.lapcevichme.winterhackathon.data.remote.AuthApiService
import kotlinx.coroutines.runBlocking
import okhttp3.Authenticator
import okhttp3.Request
import okhttp3.Response
import okhttp3.Route
import javax.inject.Inject
import javax.inject.Provider

class AuthAuthenticator @Inject constructor(
    private val tokenManager: TokenManager,
    private val apiService: Provider<AuthApiService>
) : Authenticator {

    override fun authenticate(route: Route?, response: Response): Request? {
        if (response.request.header("Authorization") == null) {
            return null
        }

        val refreshToken = tokenManager.getRefreshToken() ?: return null

        return runBlocking {
            try {
                val newTokens = apiService.get().refresh("Bearer $refreshToken")

                tokenManager.saveTokens(newTokens.accessToken, newTokens.refreshToken ?: refreshToken)

                response.request.newBuilder()
                    .header("Authorization", "Bearer ${newTokens.accessToken}")
                    .build()
            } catch (e: Exception) {
                tokenManager.clearTokens()
                null
            }
        }
    }
}