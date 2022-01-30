import React, { useEffect } from "react";
import ProductCard from "./ProductCard";
// import products from "./products";
import { Row, Col } from "react-bootstrap";
import { useSelector, useDispatch } from "react-redux";
import { listProducts } from "../../store/productsAsyncAction"; // this is async main action to use rreducer actions
import Loading from "../Loading";
import Message from "../Message";

function ProductsList() {
	// const [products, setProducts] = useState([]);
	const dispatch = useDispatch();
	const product = useSelector((state) => state.products);
	const { error, loading, products } = product; // product reducer slice has 3 parts

	useEffect(() => {
		async function loading() {
			dispatch(listProducts());
		}
		loading();
	}, [dispatch]);

	return (
		<div>
			<br />
			<h1 className='text-primary'>Latest Products</h1>
			<hr className='text-primary' />
			{loading ? (
				<Loading />
			) : error.length > 5 ? (
				<Message variant='danger'>
					<spanc className='text-light'>{error}</spanc>
				</Message>
			) : (
				<Row>
					{products.map((product) => (
						<Col
							key={product._id}
							xs={12}
							sm={12}
							md={6}
							lg={4}
							xl={4}
							xxl={3}
						>
							<ProductCard pro={product} />
						</Col>
					))}
				</Row>
			)}
		</div>
	);
}

export default ProductsList;
