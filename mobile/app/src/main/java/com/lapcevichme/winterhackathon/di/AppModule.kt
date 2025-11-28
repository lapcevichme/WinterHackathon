package com.lapcevichme.winterhackathon.di

import com.lapcevichme.winterhackathon.data.repository.mock.MockCasinoRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.mock.MockLeaderboardRepositoryImpl
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import com.lapcevichme.winterhackathon.domain.repository.LeaderboardRepository
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

    @Provides
    @Singleton
    fun provideLeaderboardRepository(): LeaderboardRepository {
        return MockLeaderboardRepositoryImpl()
    }
}