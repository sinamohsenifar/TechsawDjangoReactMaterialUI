import axios from "axios";
import axiosInstance from "../axios";
import { productActions } from "./store";

export const detailProduct = (id) => async (dispatch) => {
	dispatch(productActions.product_detail_request);

	await axiosInstance
		.get(`products/${id}`)
		.then(function (response) {
			dispatch(productActions.product_detail_success(response.data));
		})
		.catch(function (error) {
			dispatch(productActions.product_detail_fail(error.message));
		});

	// try {
	// 	dispatch(productActions.product_detail_request);

	// 	const { data } = await axios.get("/api/products/" + id);

	// 	dispatch(productActions.product_detail_success(data));
	// } catch (error) {
	// 	// error.response && error.response.data.message
	// 	// 			? error.response.data.message
	// 	// 			: error.message
	// 	dispatch(productActions.product_detail_fail(error.message));
	// }
};
