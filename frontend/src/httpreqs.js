import axios from "axios"

const baseConfig = {
    baseURL: "http://127.0.0.1:5000",
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
};

function getAPI({ url }) {
    return axios.get(url, baseConfig);
}

function getWithParamsAPI({ url, params }) {
    return axios.get(url, {
        ...baseConfig,
        params: params,
    });
}

function deleteWithParamsAPI({ url, params }) {
    return axios.delete(url, {
        ...baseConfig,
        params: params,
        paramsSerializer: {
            indexes: true
        }
    })
}

function postAPI({ url, data }) {
    return axios.post(url, data, baseConfig);
}

export { getAPI, getWithParamsAPI, postAPI, deleteWithParamsAPI };