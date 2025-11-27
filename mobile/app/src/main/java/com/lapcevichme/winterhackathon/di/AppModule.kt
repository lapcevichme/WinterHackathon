package com.lapcevichme.winterhackathon.di

import com.lapcevichme.winterhackathon.data.repository.mock.MockCasinoRepositoryImpl
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import jakarta.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideCasinoRepository(): CasinoRepository {
        return MockCasinoRepositoryImpl()
    }
}