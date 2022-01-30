import { productsActions } from "./store";
import axiosInstance from "../axios";

export const listProducts = () => async (dispatch) => {
	dispatch(productsActions.product_list_request);

	await axiosInstance
		.get("products/all")
		.then(function (response) {
			dispatch(productsActions.product_list_success(response.data));
		})
		.catch(function (error) {
			dispatch(productsActions.product_list_fail(error.message));
		});

	// const userToken = sessionStorage.getItem("userToken")
	// ? JSON.parse(sessionStorage.getItem("userToken"))
	// : null;
	// try {
	// 	dispatch(productsActions.product_list_request);
	// 	const userToken = sessionStorage.getItem("userToken")
	// 		? JSON.parse(sessionStorage.getItem("userToken"))
	// 		: null;
	// 	const { data } = sessionStorage.getItem("userToken")
	// 		? await axios.get("/api/products/all", {
	// 				headers: { Authorization: `JWT ${userToken.access}` },
	// 		  })
	// 		: await axios.get("/api/products/all");
	// 	dispatch(productsActions.product_list_success(data));
	// } catch (error) {
	// 	// error.response && error.response.data.message
	// 	// 			? error.response.data.message
	// 	// 			: error.message
	// 	dispatch(productsActions.product_list_fail(error.message));
	// }
};
