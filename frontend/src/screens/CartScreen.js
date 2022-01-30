import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { Button, Table } from "react-bootstrap";
import Message from "../components/Message";
import "./CartScreen.css";
import CartItem from "../components/CartItem";
import { cartActions } from "../store/store";
import axios from "axios";
import axiosInstance from "../axios";

function CartScreen() {
	const { id } = useParams();
	const dispatch = useDispatch();
	const cartItems = useSelector((state) => state.cart.cartItems);
	const totalPrice = useSelector((state) => state.cart.totalPrice);
	const totalItems = useSelector((state) => state.cart.totalItems);
	// here we want to notice refreshin page
	const userToken = sessionStorage.getItem("userToken")
		? JSON.parse(sessionStorage.getItem("userToken"))
		: null;

	const addToCart = () => async (dispatch, getState) => {
		await axiosInstance.get(`products/${id}`).then(function (data) {
			const item = cartItems.find((item) => item.product === `${data._id}`);
			console.log(data._id);
			if (item) {
				if (item.qty < item.maximumOrder) {
					dispatch(
						cartActions.cart_add_item({
							product: data._id,
							name: data.name,
							image: data.image,
							price: parseFloat(data.price),
							maximumOrder:
								data.countInStock > 5 ? 5 : data.countInStock,
							qty: 1,
						})
					);
					localStorage.setItem("cart", JSON.stringify(getState().cart));
				}
			} else if (data.countInStock > 0) {
				dispatch(
					cartActions.cart_add_item({
						product: data._id,
						name: data.name,
						image: data.image,
						price: parseFloat(data.price),
						maximumOrder: data.countInStock > 5 ? 5 : data.countInStock,
						qty: 1,
					})
				);
				localStorage.setItem("cart", JSON.stringify(getState().cart));
			}
		});

		// const { data } = await axios.get(`/api/products/${id}`, {
		// 	headers: { Authorization: `JWT ${userToken.access}` },
		// });
		// const item = cartItems.find((item) => item.product === `${data._id}`);
		// console.log(data._id);
		// if (item) {
		// 	if (item.qty < item.maximumOrder) {
		// 		dispatch(
		// 			cartActions.cart_add_item({
		// 				product: data._id,
		// 				name: data.name,
		// 				image: data.image,
		// 				price: parseFloat(data.price),
		// 				maximumOrder: data.countInStock > 5 ? 5 : data.countInStock,
		// 				qty: 1,
		// 			})
		// 		);
		// 		localStorage.setItem("cart", JSON.stringify(getState().cart));
		// 	}
		// } else if (data.countInStock > 0) {
		// 	dispatch(
		// 		cartActions.cart_add_item({
		// 			product: data._id,
		// 			name: data.name,
		// 			image: data.image,
		// 			price: parseFloat(data.price),
		// 			maximumOrder: data.countInStock > 5 ? 5 : data.countInStock,
		// 			qty: 1,
		// 		})
		// 	);
		// 	localStorage.setItem("cart", JSON.stringify(getState().cart));
		// }
	};

	useEffect(() => {
		if (window.performance) {
			if (performance.navigation.type !== 1) {
				if (id) {
					dispatch(addToCart(id));
				}
			}
		}
	}, [id, dispatch]);

	// const totalPrice
	return (
		<div className='text-dark'>
			<br />
			<h2>Your Cart</h2>
			<hr />
			<Table striped bordered hover variant='dark'>
				<thead>
					<tr className='text-center'>
						<th>Image</th>
						<th>Product</th>
						<th>Quantity</th>
						<th>Price</th>
						<th>Add/Remove</th>
					</tr>
				</thead>
				<tbody>
					{cartItems.map((item) => (
						<CartItem
							key={item.product}
							addHandler={addToCart}
							item={item}
						/>
					))}
				</tbody>
			</Table>
			<Table striped bordered hover variant='dark'>
				<thead>
					<tr className='text-center'>
						<th>Total Price</th>
						<th>Total Quantities</th>
						<th>Go To Payment</th>
					</tr>
				</thead>
				<tbody>
					<tr className='text-center'>
						<td>${totalPrice.toFixed(2)}</td>
						<td>{totalItems}</td>
						<td>
							<Button>Go To Proceed</Button>
						</td>
					</tr>
				</tbody>
			</Table>
		</div>
	);
}

export default CartScreen;
