import axios from "axios";

const baseUrl = "/api/";
const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));

const axiosInstance = axios.create({
	baseURL: baseUrl,
	timeout: 5000,
	headers: {
		Authorization: userInfo ? `JWT ${userInfo.access}` : null,
		"Content-Type": "application/json",
		accept: "application/json",
	},
});

export default axiosInstance;
