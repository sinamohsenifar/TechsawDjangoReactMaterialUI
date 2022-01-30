import { createSlice } from "@reduxjs/toolkit";

const cartFromStorage = localStorage.getItem("cart")
	? JSON.parse(localStorage.getItem("cart"))
	: { cartItems: [], totalItems: 0, totalPrice: 0 };

export const cartSlice = createSlice({
	name: "cart",
	initialState: cartFromStorage,
	reducers: {
		cart_add_item(state, action) {
			const item = action.payload;
			const existItem = state.cartItems.find(
				(x) => x.product === item.product
			);
			if (existItem) {
				state.cartItems.map((x) =>
					x.product === existItem.product ? x.qty++ : x.qty
				);
				state.totalPrice += existItem.price;
				state.totalItems++;
			} else {
				state.cartItems.push(item);
				state.totalPrice += item.price;
				state.totalItems++;
			}
		},
		cart_remove_item(state, action) {
			const item = action.payload;
			const existItem = state.cartItems.find(
				(x) => x.product === item.product
			);
			if (existItem && existItem.qty > 1) {
				state.cartItems.map((x) =>
					x.product === existItem.product ? x.qty-- : x.qyt
				);
				state.totalPrice -= existItem.price;
				state.totalItems--;
			} else if (existItem) {
				let cartItems = [];
				state.cartItems.map((item) =>
					item.product !== existItem.product
						? cartItems.push(item)
						: (item = {})
				);
				state.cartItems = cartItems;
				state.totalItems--;
				state.totalPrice -= existItem.price;
			}
		},
	},
});
