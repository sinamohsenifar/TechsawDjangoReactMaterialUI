import React, { useState, useEffect } from "react";
import { Container, Form, Button, Row, Col } from "react-bootstrap";
// import axios from "axios";
import { Navigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { userLogin } from "../store/usersAsyncAction";
import Message from "../components/Message";
import axiosInstance from "../axios";

function LoginScreen() {
	const [user, setUser] = useState({
		username: "",
		password: "",
	});
	const userInfo = useSelector((state) => state.user);
	const dispatch = useDispatch();

	const handleChange = (event) => {
		setUser({ ...user, [event.target.name]: event.target.value });
	};

	const LoginHandler = () => {
		dispatch(userLogin(user.username, user.password));
	};
	const [verifyUsername, setVerifyUsername] = useState(false);
	const [verifyUsernameAlarm, setVerifyUsernameAlarm] = useState(false);

	useEffect(() => {}, []);

	async function handleUserVerify() {
		if (user.username.length >= 3) {
			await axiosInstance
				.get(`users/verifyusername/?username=${user.username}`)
				.then(function (response) {
					if (response.data.message === false) {
						setVerifyUsername(true);
						setVerifyUsernameAlarm(false);
					} else {
						setVerifyUsername(false);
						setVerifyUsernameAlarm(true);
					}
				});
		} else {
			setVerifyUsername(false);
			setVerifyUsernameAlarm(true);
		}
	}

	// async function LoginHandler() {
	// 	sessionStorage.removeItem("userToken");
	// 	await axiosInstance
	// 		.post("users/token/", {
	// 			username: user.username,
	// 			password: user.password,
	// 		})
	// 		.then(function (response) {
	// 			setLoggedIn(true);
	// 			console.log("this is first message");
	// 			sessionStorage.setItem("userToken", JSON.stringify(response.data));
	// 			console.log(response.data);
	// 		})
	// 		.catch(function (error) {
	// 			console.log("this is error message");
	// 			sessionStorage.removeItem("userToken");
	// 			console.log(error);
	// 		})
	// 		.then(function () {
	// 			console.log("you alwayse see this message");
	// 		});
	// }

	// async function Login() {
	// 	try {
	// 		const { data } = await axiosInstance.post("users/token/", {
	// 			username: user.username,
	// 			password: user.password,
	// 		});
	// 		if (data === undefined) {
	// 			console.log("the username or password is wrong");
	// 		} else {
	// 			sessionStorage.setItem("userToken", JSON.stringify(data));
	// 			document.getElementById("formBasicEmail").value = "";
	// 			document.getElementById("formBasicPassword").value = "";
	// 		}
	// 	} catch (error) {
	// 		console.log(error);
	// 	}
	// }

	// useEffect(() => {
	// 	const userToken = JSON.parse(sessionStorage.getItem("userToken"));
	// });

	return (
		<div id='RegisterForm'>
			<br />
			{userInfo.loginStatus && <Navigate to='/' />}
			{userInfo.error.data && (
				<Message variant='danger'>
					{!verifyUsername && <li>username is Not Valid</li>}
					{userInfo.error.data.detail && (
						<li>username or password is Not Valid</li>
					)}
				</Message>
			)}
			<Container>
				<Row className=' p-4'>
					<Col>
						<Form className='p-4 bg-info rounded'>
							<Form.Group className='mb-3' controlId='formBasicEmail'>
								<Form.Label className='text-light'>Username</Form.Label>
								<Form.Control
									onChange={handleChange}
									name='username'
									type='text'
									placeholder='Enter username'
								/>
								{verifyUsernameAlarm && (
									<Form.Text className='text-muted'>
										<p className='text-light'>
											<span className='text-danger'>
												<i className='fas fa-times-circle'></i>
											</span>
											This Username Is Not Valid
										</p>
									</Form.Text>
								)}
								{verifyUsername && (
									<Form.Text className='text-muted'>
										<p className='text-light'>
											<span className='text-success'>
												<i className='fas fa-check-circle'></i>
											</span>
											Okay
										</p>
									</Form.Text>
								)}
								<Form.Text className='text-muted'></Form.Text>
							</Form.Group>
							<Form.Group className='mb-3' controlId='formBasicPassword'>
								<Form.Label className='text-light'>Password</Form.Label>
								<Form.Control
									onFocus={handleUserVerify}
									onChange={handleChange}
									name='password'
									type='password'
									placeholder='Password'
								/>
								<Form.Text className='text-muted'></Form.Text>
							</Form.Group>
							<Form.Group className='mb-3' controlId='formBasicCheckbox'>
								<Form.Check
									className='text-light'
									type='checkbox'
									label='With this i remember you for at least a day'
								/>
							</Form.Group>

							<Button
								onClick={LoginHandler}
								variant='success'
								type='button'
							>
								Log In
							</Button>
						</Form>
					</Col>
				</Row>
			</Container>
		</div>
	);
}

export default LoginScreen;
