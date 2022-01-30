import React, { useEffect } from "react";
import {
	Navbar,
	Container,
	Nav,
	Form,
	FormControl,
	Button,
	NavDropdown,
} from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { userActions } from "../store/store";

function Header() {
	const userInfo = useSelector((state) => state.user);
	const dispatch = useDispatch();

	const logoutHandler = () => {
		sessionStorage.removeItem("userInfo");
		dispatch(userActions.user_logout());
	};
	useEffect(() => {});
	return (
		<div>
			<Navbar bg='dark' variant='dark' expand='md'>
				<Container fluid>
					<LinkContainer to='/'>
						<Navbar.Brand>
							<span className='text-light'>Cena SHOP</span>
						</Navbar.Brand>
					</LinkContainer>
					<Navbar.Toggle aria-controls='navbarScroll' />
					<Navbar.Collapse id='navbarScroll'>
						<Nav
							className='me-auto my-2 my-lg-0'
							style={{ maxHeight: "200px" }}
							navbarScroll
						>
							{userInfo.loginStatus && (
								<NavDropdown
									title={
										<span className='text-success'>
											{userInfo.user.username}
										</span>
									}
									id='basic-nav-dropdown'
								>
									<LinkContainer to='/'>
										<Nav.Link
											className='mx-2'
											onClick={logoutHandler}
										>
											<i className='text-success fas  fa-sign-out-alt'></i>
											<span className='text-secondary'>
												{" "}
												Log Out
											</span>
										</Nav.Link>
									</LinkContainer>
									<LinkContainer to='/dashboard'>
										<Nav.Link className='mx-2'>
											<i className='text-success fas fa-address-card'></i>
											<span className='text-secondary'>
												{" "}
												Dashboard
											</span>
										</Nav.Link>
									</LinkContainer>

									<NavDropdown.Item href='#action/3.3'>
										Something
									</NavDropdown.Item>
									<NavDropdown.Divider />
									<LinkContainer to='/cart/'>
										<Nav.Link className='mx-2'>
											<i className='fas fa-cart-shopping text-success'></i>
											<span className='text-secondary'>Cart</span>
										</Nav.Link>
									</LinkContainer>
								</NavDropdown>
							)}

							{!userInfo.loginStatus && (
								<LinkContainer to='/login'>
									<Nav.Link>
										<i className='text-success fas fa-user'></i>
										<span className='text-light'> Login</span>
									</Nav.Link>
								</LinkContainer>
							)}

							{!userInfo.loginStatus && (
								<LinkContainer to='/signup'>
									<Nav.Link>
										<i className='text-success fas fa-user'></i>
										<span className='text-light'> SignUp</span>
									</Nav.Link>
								</LinkContainer>
							)}
						</Nav>
						<Form className='d-flex'>
							<FormControl
								type='search'
								placeholder='Search'
								className='me-2 bg-success'
								aria-label='Search'
							/>
							<Button className='btn btn-success'>Search</Button>
						</Form>
					</Navbar.Collapse>
				</Container>
			</Navbar>
		</div>
	);
}

export default Header;
