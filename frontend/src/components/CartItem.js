import React from "react";
import { Image, Button, ButtonGroup } from "react-bootstrap";
import { useDispatch } from "react-redux";
import { cartActions } from "../store/store";
import { Link } from "react-router-dom";

function CartItem({ item }) {
	const addToCart = () => async (dispatch, getState) => {
		dispatch(
			cartActions.cart_add_item({
				product: item.product,
				name: item.name,
				image: item.image,
				price: parseFloat(item.price),
				qty: 1,
			})
		);
		localStorage.setItem("cart", JSON.stringify(getState().cart));
	};
	const removeFromCart = () => async (dispatch, getState) => {
		dispatch(
			cartActions.cart_remove_item({
				product: item.product,
				name: item.name,
				image: item.image,
				price: parseFloat(item.price),
				qty: 1,
			})
		);
		localStorage.setItem("cart", JSON.stringify(getState().cart));
	};

	const dispatch = useDispatch();
	const addToCartHandler = () => {
		dispatch(addToCart(item.product));
	};
	const RemoveFromCartHandler = () => {
		dispatch(removeFromCart(item.product));
	};
	return (
		<tr className='text-center centerize'>
			<td>
				<Link to={"/product/" + item.product}>
					<Image src={item.image} alt={item.name} fluid width={80} />
				</Link>
			</td>
			<td className='text-center'>
				<Link
					className='text-decoration-none text-light'
					to={"/product/" + item.product}
				>
					{item.name}
				</Link>
			</td>
			<td>{item.qty}</td>
			<td>{item.price}</td>
			<td>
				<ButtonGroup>
					{item.qty < item.maximumOrder && (
						<Button onClick={addToCartHandler}>Add</Button>
					)}
					<Button onClick={RemoveFromCartHandler}>Remove</Button>
				</ButtonGroup>
			</td>
		</tr>
	);
}

export default CartItem;
