import axios from "axios";

import { API_BASE_URL } from "../utils/constants";
import { getAccessToken } from "../services/authService";

const apiClient = axios.create({

    baseURL: API_BASE_URL,

});

apiClient.interceptors.request.use(

    async (config) => {

        const token = await getAccessToken();

        if (token) {

            config.headers.Authorization =
                `Bearer ${token}`;

        }

        return config;

    }

);

export default apiClient;