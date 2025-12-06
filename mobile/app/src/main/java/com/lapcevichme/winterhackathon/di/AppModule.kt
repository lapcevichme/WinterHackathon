package com.lapcevichme.winterhackathon.di

import com.lapcevichme.winterhackathon.data.remote.MainApiService
import com.lapcevichme.winterhackathon.data.remote.UserApiService
import com.lapcevichme.winterhackathon.data.repository.impl.AdminRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.impl.CasinoRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.impl.GameRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.impl.LeaderboardRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.impl.MainRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.impl.ProfileRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.impl.UserRepositoryImpl
import com.lapcevichme.winterhackathon.data.repository.mock.MockMainRepositoryImpl
import com.lapcevichme.winterhackathon.domain.repository.AdminRepository
import com.lapcevichme.winterhackathon.domain.repository.CasinoRepository
import com.lapcevichme.winterhackathon.domain.repository.GameRepository
import com.lapcevichme.winterhackathon.domain.repository.LeaderboardRepository
import com.lapcevichme.winterhackathon.domain.repository.MainRepository
import com.lapcevichme.winterhackathon.domain.repository.ProfileRepository
import com.lapcevichme.winterhackathon.domain.repository.UserRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import retrofit2.Retrofit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideCasinoRepository(impl: CasinoRepositoryImpl): CasinoRepository {
        return impl
    }

    @Provides
    @Singleton
    fun provideLeaderboardRepository(impl: LeaderboardRepositoryImpl): LeaderboardRepository {
        return impl
    }

    @Provides
    @Singleton
    fun provideProfileRepository(impl: ProfileRepositoryImpl): ProfileRepository {
        return impl
    }

    @Provides
    @Singleton
    fun provideGameRepository(impl: GameRepositoryImpl): GameRepository {
        return impl
    }

    @Provides
    @Singleton
    fun provideMainRepository(impl: MainRepositoryImpl): MainRepository {
        return impl
    }

    @Provides
    @Singleton
    fun provideAdminRepository(impl: AdminRepositoryImpl): AdminRepository {
        return impl
    }

    @Provides
    @Singleton
    fun provideUserRepository(impl: UserRepositoryImpl): UserRepository {
        return impl
    }

    @Provides
    @Singleton
    fun provideTeamRepository(impl: com.lapcevichme.winterhackathon.data.repository.impl.TeamRepositoryImpl): com.lapcevichme.winterhackathon.domain.repository.TeamRepository {
        return impl
    }
}