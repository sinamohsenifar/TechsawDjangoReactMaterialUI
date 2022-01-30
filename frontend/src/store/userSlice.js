import { createSlice } from "@reduxjs/toolkit";

// const initialState = {
// 	user: {},
// 	loading: false,
// 	error: {},
// 	loginStatus: false,
// };
const initialState = sessionStorage.getItem("userInfo")
	? {
			user: JSON.parse(sessionStorage.getItem("userInfo")),
			loading: false,
			error: {},
			loginStatus: true,
	  }
	: {
			user: {},
			loading: false,
			error: {},
			loginStatus: false,
	  };

export const userSlice = createSlice({
	name: "users",
	initialState,
	reducers: {
		user_login_request(state) {
			state.loading = true;
			state.user = {};
			state.loginStatus = false;
			state.error = {};
			sessionStorage.removeItem("userInfo");
		},
		user_login_success(state, action) {
			state.loading = false;
			state.user = action.payload;
			state.loginStatus = true;
			state.error = {};
			sessionStorage.setItem("userInfo", JSON.stringify(state.user));
		},
		user_login_fail(state, action) {
			state.loading = false;
			state.error = action.payload;
			state.loginStatus = false;
			sessionStorage.removeItem("userInfo");
		},
		user_logout(state) {
			state.loading = false;
			state.user = {};
			state.loginStatus = false;
			state.error = {};
			sessionStorage.removeItem("userInfo");
		},
		user_signup_request(state) {
			state.loading = true;
			state.user = {};
			state.loginStatus = false;
			state.error = {};
			sessionStorage.removeItem("userInfo");
		},
		user_signup_success(state, action) {
			state.loading = false;
			state.user = action.payload;
			state.loginStatus = true;
			state.error = {};
			sessionStorage.setItem("userInfo", JSON.stringify(state.user));
		},
		user_signup_fail(state, action) {
			state.loading = false;
			state.user = {};
			state.error = action.payload;
			state.loginStatus = false;
			sessionStorage.removeItem("userInfo");
		},
		// Update User
		user_update_request(state) {
			state.loading = true;
			state.loginStatus = true;
			state.error = {};
		},
		user_update_success(state, action) {
			state.loading = false;
			state.user = action.payload;
			state.loginStatus = true;
			state.error = {};
			sessionStorage.setItem("userInfo", JSON.stringify(state.user));
		},
		user_update_fail(state, action) {
			state.loading = false;
			state.error = action.payload;
		},
	},
});
