import { createSlice } from "@reduxjs/toolkit";

const initialState = { products: [], loading: false, error: {}, product: {} };

export const productsSlice = createSlice({
	name: "products",
	initialState,
	reducers: {
		product_list_request(state) {
			state.loading = true;
			state.products = [];
		},
		product_list_success(state, action) {
			state.loading = false;
			state.products = action.payload;
		},
		product_list_fail(state, action) {
			state.loading = false;
			state.error = action.payload;
		},
	},
});
