import axios from "axios";
import { getAPI, postAPI } from "./httpreqs";
import { useRouter } from "vue-router";

// HELPFUL FUNCTIONS USED THROUGHOUT APP

async function loginUser(credentials) {
    const response = await postAPI({ url: "/core/login", data: credentials });
    if (response.data.logged_in) {
        localStorage.setItem("JWT", response.data.access_token);
        localStorage.setItem("EMAIL", response.data.useremail);
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

function sameLoggedinUser(email) {
    // const usercreds = await checkAuth();
    if (localStorage.getItem("EMAIL") === email) {
        return true;
    }
    return false;
}

// async function handleRedirect() {

// }

function logoutUser() {
    localStorage.removeItem("JWT");
    localStorage.removeItem("EMAIL");
    return { logged_in: false };
}

export { loginUser, checkAuth, logoutUser, sameLoggedinUser };