import { userActions } from "./store";
import axiosInstance from "../axios";

export const userLogin = (username, password) => async (dispatch) => {
	dispatch(userActions.user_login_request);

	await axiosInstance
		.post("users/token/", {
			username: username,
			password: password,
		})
		.then(function (response) {
			console.log("this is first message");
			sessionStorage.setItem("userInfo", JSON.stringify(response.data));
			dispatch(userActions.user_login_success(response.data));
			// sessionStorage.setItem("userToken", JSON.stringify(response.data));
			// console.log(response.data);
		})
		.catch(function (error) {
			console.log("this is error message");
			console.log(error.response);
			dispatch(userActions.user_login_fail(error.response));
			// sessionStorage.removeItem("userToken");
			// console.log(error);
		})
		.then(function (response) {
			console.log(response);
		});
};

// export const userLogout = () => async (dispatch) => {
// 	sessionStorage.removeItem("userInfo");
// 	dispatch(userActions.user_logout());
// 	// await axiosInstance
// 	// 	.post("users/logout/", {
// 	// 		refresh_token: refresh,
// 	// 	})
// 	// 	.then(function (response) {
// 	// 		sessionStorage.removeItem("userToken");
// 	// 		console.log("this is first message");
// 	// 		console.log(response.data);
// 	// 		dispatch(userActions.user_logout());
// 	// 		axiosInstance.defaults.headers["Authorization"] = null;
// 	// 	})
// 	// 	.catch(function (error) {
// 	// 		console.log("this is error message");
// 	// 		console.log(error);
// 	// 	})
// 	// 	.then(function () {
// 	// 		console.log("you alwayse see this message");
// 	// 	});
// };

export const userRegister = (email, username, password) => async (dispatch) => {
	dispatch(userActions.user_login_request);

	await axiosInstance
		.post("users/registration/", {
			email: email,
			username: username,
			password: password,
		})
		.then(function (response) {
			console.log("this is first message");
			dispatch(userActions.user_login_success(response.data));
			// sessionStorage.setItem("userToken", JSON.stringify(response.data));
			// console.log(response.data);
		})
		.catch(function (error) {
			console.log("this is error message");
			console.log(error.response);
			console.log("this is error message");
			console.log(error.data);
			console.log("this is error message");
			console.log(error.detail);
			dispatch(userActions.user_login_fail(error.response));
			// sessionStorage.removeItem("userToken");
			// console.log(error);
		})
		.then(function (response) {
			console.log(response);
		});
};

export const userUpdate = (update_user) => async (dispatch) => {
	const [email, username, image, password, first_name, last_name] =
		update_user;

	dispatch(userActions.user_update_request);

	await axiosInstance
		.put("users/profile/update", {
			email: email,
			username: username,
			password: password,
			first_name: first_name,
			last_name: last_name,
			image: image,
		})
		.then(function (response) {
			console.log("this is first message");
			dispatch(userActions.user_update_success(response.data));
			// sessionStorage.setItem("userToken", JSON.stringify(response.data));
			// console.log(response.data);
		})
		.catch(function (error) {
			console.log("this is error message");
			console.log(error.response);

			dispatch(userActions.user_update_fail(error.response));
			// sessionStorage.removeItem("userToken");
			// console.log(error);
		})
		.then(function (response) {});
};
