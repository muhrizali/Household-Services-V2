import axios from "axios";
import { getAPI, postAPI } from "./httpreqs";

// HELPFUL FUNCTIONS USED THROUGHOUT APP

async function loginUser(credentials) {
    const response = await postAPI({ url: "/core/login", data: credentials });
    if (response.data.logged_in) {
        localStorage.setItem("JWT", response.data.access_token);
        return { message: "Login Successful", ...response.data };
    } else {
        return { message: "Login Failed", ...response.data };
    }
}

async function checkAuth() {
    const token = localStorage.getItem("JWT");
    if (!token) {
        return { logged_in: false };
    }
    const response = await axios.get("/core/protected", {
        baseURL: "http://127.0.0.1:5000",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        withCredentials: true,
    });
    if (response.data.logged_in) {
        return response.data;
    } else {
        return { logged_in: false };
    }
}

// async function handleRedirect() {

// }

function logoutUser() {
    localStorage.removeItem("JWT");
    return { logged_in: false };
}

export { loginUser, checkAuth, logoutUser };