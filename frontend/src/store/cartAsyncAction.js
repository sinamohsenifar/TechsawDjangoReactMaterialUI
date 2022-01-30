import axios from "axios";
import { cartActions } from "./store";

export const addToCart = (id) => async (dispatch, getState) => {
	const { data } = await axios.get(`/api/products/${id}`);

	dispatch(
		cartActions.cart_add_item({
			product: data._id,
			name: data.name,
			image: data.image,
			price: parseFloat(data.price),
			qty: 1,
		})
	);
	localStorage.setItem("cart", JSON.stringify(getState().cart));
};

export const removeFromCart = (id) => async (dispatch, getState) => {
	const { data } = await axios.get(`/api/products/${id}`);

	dispatch(
		cartActions.cart_remove_item({
			product: id,
			name: data.name,
			image: data.image,
			price: parseFloat(data.price),
			qty: 1,
		})
	);
	localStorage.setItem("cart", JSON.stringify(getState().cart));
};
