package com.lapcevichme.winterhackathon.di

import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import com.lapcevichme.winterhackathon.data.remote.CasinoApiService
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import retrofit2.Retrofit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    private const val BASE_URL = "" // TODO IMPLEMENT BASE URL!!!

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        val json = Json {
            ignoreUnknownKeys = true
            coerceInputValues = true
        }

        val contentType = "application/json".toMediaType()

        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(json.asConverterFactory(contentType))
            .build()
    }

    @Provides
    @Singleton
    fun provideCasinoApi(retrofit: Retrofit): CasinoApiService {
        return retrofit.create(CasinoApiService::class.java)
    }
}