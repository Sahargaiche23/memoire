import axios from 'axios';

// Configuration globale d'Axios pour JWT
const setupAxiosInterceptors = () => {
  // Intercepteur pour les requêtes sortantes
  axios.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Intercepteur pour les réponses
  axios.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      if (error.response?.status === 401) {
        // Token expiré ou invalide
        console.warn('Token JWT invalide ou expiré');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        // Rediriger vers login
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );
};

export default setupAxiosInterceptors;
