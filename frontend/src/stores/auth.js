import { defineStore } from 'pinia'
import axios from '../axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: localStorage.getItem('accessToken') || null,
        refreshToken: localStorage.getItem('refreshToken') || null,
        user: null,
        error: null,
        loading: false
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken
    },
    actions: {
        setToken(token) {
            this.accessToken = token;
            localStorage.setItem('accessToken', token);
        },
        clearAuthData() {
            this.accessToken = null;
            localStorage.removeItem('accessToken');
            this.user = null;
        },
        async login(credentials) {
            this.error = null
            this.loading = true
            try {
                const response = await axios.post('http://localhost:8000/api/users/auth/jwt/create', credentials)
                const { access, refresh } = response.data
                this.setToken(access)
                localStorage.setItem('refreshToken', refresh)
                this.refreshToken = refresh

                await this.fetchUser()
            } catch (error) {
                this.error = error.response?.data || 'Login failed'
            } finally {
                this.loading = false
            }
        },
        async register(formData) {
            this.error = null
            this.loading = true
            try {
                await axios.post('http://localhost:8000/api/users/auth/users/', formData)
                // После успешной регистрации можно перенаправить на login или
                // автоматически залогинить, если API это позволяет.
            } catch (error) {
                this.error = error.response?.data || 'Registration failed'
            } finally {
                this.loading = false
            }
        },
        async resetPassword(email) {
            this.error = null
            this.loading = true
            try {
                await axios.post('http://localhost:8000/api/users/auth/users/reset_password/', { email })
                // На почту будет выслана ссылка для сброса пароля.
                // Отдельная логика для подтверждения сброса (reset_password_confirm) вам понадобится на отдельной странице.
            } catch (error) {
                this.error = error.response?.data || 'Reset password failed'
            } finally {
                this.loading = false
            }
        },
        async resetPasswordConfirm(uid, token, new_password, re_new_password) {
            this.error = null
            this.loading = true
            try {
                await axios.post('http://localhost:8000/api/users/auth/users/reset_password_confirm/', {
                    uid,
                    token,
                    new_password,
                    re_new_password
                })
                // После успешного сброса можно перенаправить на /login
            } catch (error) {
                this.error = error.response?.data || 'Reset password confirm failed'
            } finally {
                this.loading = false
            }
        },
        async fetchUser() {
            this.error = null
            this.loading = true
            try {
                const response = await axios.get('http://localhost:8000/api/users/auth/users/me/', {
                    headers: {
                        Authorization: `Bearer ${this.accessToken}`
                    }
                })
                this.user = response.data
            } catch (error) {
                this.error = error.response?.data || 'Fetch user failed'
            } finally {
                this.loading = false
            }
        },
        logout() {
            this.clearAuthData()
        }
    }
})
