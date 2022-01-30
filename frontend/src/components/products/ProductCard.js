import React from "react";
import { Card } from "react-bootstrap";
import Rating from "../Rating";
import { Link } from "react-router-dom";
const ProductCard = (props) => {
	const product = props.pro;
	return (
		<Card className='my-1 mx-1 py-1 px-1 rounded'>
			<Link to={"/product/" + product._id}>
				<Card.Img variant='top' src={product.image} />
			</Link>
			<Card.Body className='text-dark '>
				<Link className='text-primary' to={"/product/" + product._id}>
					<Card.Title>{product.name}</Card.Title>
				</Link>
				<Card.Text>{product.description.substring(0, 100)}...</Card.Text>
			</Card.Body>
			<Rating
				className='my-1'
				value={product.rating}
				text={String("  from " + product.numReviews + " reviews")}
				color={"#ffea00"}
			/>
			<strong className='text-dark'>Price : ${product.price}</strong>

			<Link className='btn bg-success ' to={"/product/" + product._id}>
				<span className='text-light'>See More</span>
			</Link>
		</Card>
	);
};

export default ProductCard;
