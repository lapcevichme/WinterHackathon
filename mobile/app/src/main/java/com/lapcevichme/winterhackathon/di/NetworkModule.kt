package com.lapcevichme.winterhackathon.di

import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import com.lapcevichme.winterhackathon.core.network.AuthAuthenticator
import com.lapcevichme.winterhackathon.core.network.AuthInterceptor
import com.lapcevichme.winterhackathon.data.remote.AdminApiService
import com.lapcevichme.winterhackathon.data.remote.CasinoApiService
import com.lapcevichme.winterhackathon.data.remote.GameApiService
import com.lapcevichme.winterhackathon.data.remote.LeaderboardApiService
import com.lapcevichme.winterhackathon.data.remote.MainApiService
import com.lapcevichme.winterhackathon.data.remote.ProfileApiService
import com.lapcevichme.winterhackathon.data.remote.UserApiService
import com.lapcevichme.winterhackathon.data.repository.impl.MainRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.impl.UserRepositoryImpl
import com.lapcevichme.winterhackathon.domain.repository.MainRepository
import com.lapcevichme.winterhackathon.domain.repository.UserRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    private const val BASE_URL = "https://winter-hack.fly.dev/api/v1/"

    @Provides
    @Singleton
    fun provideOkHttpClient(
        authInterceptor: AuthInterceptor,
        authAuthenticator: AuthAuthenticator
    ): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .authenticator(authAuthenticator)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        val json = Json {
            ignoreUnknownKeys = true
            coerceInputValues = true
        }

        val contentType = "application/json".toMediaType()

        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(json.asConverterFactory(contentType))
            .build()
    }

    @Provides
    @Singleton
    fun provideCasinoApi(retrofit: Retrofit): CasinoApiService {
        return retrofit.create(CasinoApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideGameApiService(retrofit: Retrofit): GameApiService {
        return retrofit.create(GameApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideLeaderboardApi(retrofit: Retrofit): LeaderboardApiService {
        return retrofit.create(LeaderboardApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideProfileApi(retrofit: Retrofit): ProfileApiService {
        return retrofit.create(ProfileApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideAdminApiService(retrofit: Retrofit): AdminApiService {
        return retrofit.create(AdminApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideUserApiService(retrofit: Retrofit): UserApiService {
        return retrofit.create(UserApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideMainApiService(retrofit: Retrofit): MainApiService {
        return retrofit.create(MainApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideTeamApiService(retrofit: Retrofit): com.lapcevichme.winterhackathon.data.remote.TeamApiService {
        return retrofit.create(com.lapcevichme.winterhackathon.data.remote.TeamApiService::class.java)
    }
}