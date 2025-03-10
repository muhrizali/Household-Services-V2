import axios from "axios";

const baseConfig = {
    baseURL: "http://127.0.0.1:5000",
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
};

async function getAPI({ url, params }) {
    if (params) {
        return await axios.get(url, { ...baseConfig, params });
    }
    return await axios.get(url, { ...baseConfig });
}


async function getWithParamsAPI({ url, params }) {
    return await axios.get(url, { ...baseConfig, params });
}

async function deleteAPI({ url, params }) {
    if (params) {
        return await axios.delete(url, { 
            ...baseConfig,
            params,
            paramsSerializer: {
                indexes: null
            }
        });
    }
    return await axios.delete(url, baseConfig);

}

async function postAPI({ url, data }) {
    return await axios.post(url, data, baseConfig);
}

async function putAPI({ url, data }) {
    return await axios.put(url, data, baseConfig);
}

export { getAPI, getWithParamsAPI, postAPI, putAPI, deleteAPI };