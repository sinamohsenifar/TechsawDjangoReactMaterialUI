import { configureStore } from "@reduxjs/toolkit";
import { productsSlice } from "./productsSlice";
import { productSlice } from "./productSlice";
import { cartSlice } from "./cartSlice";
import { userSlice } from "./userSlice";
const store = configureStore({
	reducer: {
		products: productsSlice.reducer,
		product: productSlice.reducer,
		cart: cartSlice.reducer,
		user: userSlice.reducer,
	},
});

// const cartItemsFromStorage = localStorage.getItem("cartItems")
// 	? JSON.parse(localStorage.getItem("cartItems"))
// 	: [];

// const useInfoFromStorage = sessionStorage.getItem("userInfo")
// 	? JSON.parse(sessionStorage.getItem("userInfo"))
// 	: null;

export const productsActions = productsSlice.actions;
export const productActions = productSlice.actions;
export const cartActions = cartSlice.actions;
export const userActions = userSlice.actions;

export default store;
