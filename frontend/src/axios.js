import axios from 'axios'

const instance = axios.create({
    baseURL: 'http://localhost:8000/api/users/',
    timeout: 5000
})

instance.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            const authStore = useAuthStore()
            authStore.logout()
            // Возможно, перенаправить на /login
        }
        return Promise.reject(error)
    }
)

export default instance
