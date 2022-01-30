import { createSlice } from "@reduxjs/toolkit";

const initialState = { product: {}, loading: false, error: {} };

export const productSlice = createSlice({
	name: "products",
	initialState,
	reducers: {
		product_detail_request(state) {
			state.loading = true;
			state.product = {};
		},
		product_detail_success(state, action) {
			state.loading = false;
			state.product = action.payload;
		},
		product_detail_fail(state, action) {
			state.loading = false;
			state.error = action.payload;
		},
	},
});
