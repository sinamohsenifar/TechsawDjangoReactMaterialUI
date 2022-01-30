import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { Row, Col, Image, ListGroup, Button } from "react-bootstrap";
import Rating from "../components/Rating";
import { useDispatch, useSelector } from "react-redux";
import { detailProduct } from "../store/productAsyncAction";
import Loading from "../components/Loading";
import Message from "../components/Message";
import { Link } from "react-router-dom";

export default function ProductScreen() {
	// const navigate = useNavigate();

	const { id } = useParams();
	const dispatch = useDispatch();

	// const [product, setProduct] = useState([]);
	useEffect(() => {
		// async function fetchProduct() {
		// 	const { data } = await axios.get(`/api/products/${id}`);
		// 	setProduct(data);
		// }
		// fetchProduct();
		dispatch(detailProduct(id));
	}, [id, dispatch]);

	const prouctdetail = useSelector((state) => state.product);
	const { error, loading, product } = prouctdetail;

	// const maxQuantity = 5;
	// const minQuantity = 1;
	// const quantities = [];
	// if (maxQuantity < product.countInStock) {
	// 	for (let i = minQuantity; i <= maxQuantity; i++) {
	// 		quantities.push(i);
	// 	}
	// } else {
	// 	for (let i = minQuantity; i <= product.countInStock; i++) {
	// 		quantities.push(i);
	// 	}
	// }

	return (
		<React.Fragment>
			<div>
				<br />
				<h1 className='text-primary'>Latest Products</h1>
				<hr className='text-primary' />
				{loading ? (
					<Loading />
				) : error.length > 5 ? (
					<Message variant='danger'>{error}</Message>
				) : (
					<Row>
						<Col xs={12} sm={12} md={6} lg={6} xl={6} xxl={5}>
							<ListGroup>
								<ListGroup.Item className='text-dark'>
									<h2>
										<small>{product.name}</small>
									</h2>
								</ListGroup.Item>
								<ListGroup.Item className='text-dark'>
									<Image
										src={product.image}
										alt={product.name}
										fluid
									/>
								</ListGroup.Item>
							</ListGroup>
						</Col>

						<Col xs={12} sm={12} md={6} lg={6} xl={6} xxl={7}>
							<ListGroup>
								<ListGroup.Item className='text-dark'>
									<h3>
										<small>{product.description}</small>
									</h3>
								</ListGroup.Item>
								<ListGroup.Item className='text-dark text-center'>
									<Row>
										<Col>
											<span className='text-dark'>Price :</span>
										</Col>
										<Col>${product.price}</Col>
									</Row>
								</ListGroup.Item>
								<ListGroup.Item className='text-dark text-center'>
									<Row>
										<Col>
											<span className='text-dark'>Status :</span>
										</Col>
										<Col>
											{product.countInStock > 0 &&
												product.countInStock +
													"  Product In Stock  "}
											{product.countInStock === 0 && "Out Of Stock"}
										</Col>
									</Row>
								</ListGroup.Item>
								<ListGroup.Item>
									<Rating
										className='my-1'
										value={product.rating}
										text={String(
											"  from " + product.numReviews + " reviews"
										)}
										color={"#ffea00"}
									/>
								</ListGroup.Item>
								{product.countInStock > 0 && (
									<ListGroup.Item>
										<Row className='align-items-start'>
											<Col
												className='align-self-center'
												xs={3}
												sm={3}
												md={4}
												lg={3}
												xl={3}
												xxl={2}
											></Col>
										</Row>
									</ListGroup.Item>
								)}
								{product.countInStock > 0 && (
									<ListGroup.Item>
										<Link
											className={`text-light text-decoration-none`}
											to={"/cart/" + id}
										>
											<Row>
												<Button
													className='btn btn-block'
													disabled={product.countInStock === 0}
												>
													Add To Cart
												</Button>
											</Row>
										</Link>
									</ListGroup.Item>
								)}
							</ListGroup>
						</Col>
					</Row>
				)}
			</div>
		</React.Fragment>
	);
}
