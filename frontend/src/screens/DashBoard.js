import React, { useState, useEffect } from "react";
import { Container, Form, Button, Row, Col } from "react-bootstrap";
import { Navigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { userUpdate } from "../store/usersAsyncAction";
import Message from "../components/Message";
import axiosInstance from "../axios";
import { userActions } from "../store/store";

function DashBoard() {
	const [updateMessage, setUpdateMessage] = useState(false);

	// const userInfo = useSelector((state) => state.user);
	const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));

	const dispatch = useDispatch();

	const [verifyEmail, setVerifyEmail] = useState(false);
	const [verifyUsername, setVerifyUsername] = useState(false);
	const [verifypasswords, setVeriftPasswords] = useState(false);

	const [verifyEmailAlarm, setVerifyEmailAlarm] = useState(false);
	const [verifyUsernameAlarm, setVerifyUsernameAlarm] = useState(false);
	const [updated, setUpdated] = useState(false);

	const [user, setUser] = useState({
		username: userInfo.username,
		email: userInfo.email,
		first_name: userInfo.first_name,
		last_name: userInfo.last_name,
		password: "",
		password2: "",
	});
	const handleChange = (event) => {
		setUser({ ...user, [event.target.name]: event.target.value });
	};

	// useEffect(() => {});

	async function UpdateProfileHandler() {
		if (user.password === user.password2 && verifyEmail && verifyUsername) {
			setUpdateMessage(false);
			const update_user = {
				username: user.username,
				email: user.email,
				first_name: user.first_name,
				last_name: user.last_name,
				password: user.password,
				image: userInfo.image,
			};
			dispatch(userUpdate(update_user));
			setUpdated(true);
			// await axiosInstance
			// 	.post("users/registration/", {
			// 		email: user.email,
			// 		username: user.username,
			// 		password: user.password,
			// 	})
			// 	.then(function (response) {
			// 		console.log("this is first message");
			// 		console.log(response);
			// 	})
			// 	.catch(function (error) {
			// 		console.log("this is error message");
			// 		console.log(error);
			// 	})
			// 	.then(function () {
			// 		console.log("you alwayse see this message");
			// 	});
		} else {
			setUpdateMessage(true);
		}
	}
	async function checkEmailHandler() {
		if (user.email === userInfo.email) {
			setVerifyEmail(true);
			setVerifyEmailAlarm(false);
		} else if (user.email.length > 7) {
			await axiosInstance
				.get(`users/verifyemail/?email=${user.email}`)
				.then(function (response) {
					console.log(response);
					if (response.data.message === true) {
						console.log("this email is okay");
						setVerifyEmail(true);
						setVerifyEmailAlarm(false);
					} else {
						console.log("this email is NOT okay");
						setVerifyEmail(false);
						setVerifyEmailAlarm(true);
					}
				});
		} else {
			setVerifyEmail(false);
			setVerifyEmailAlarm(true);
		}
	}
	async function checkUsernameHandler() {
		if (user.username === userInfo.username) {
			setVerifyUsername(true);
			setVerifyUsernameAlarm(false);
		} else if (user.username.length >= 3) {
			await axiosInstance
				.get(`users/verifyusername/?username=${user.username}`)
				.then(function (response) {
					if (response.data.message === true) {
						console.log("this username is okay");
						setVerifyUsername(true);
						setVerifyUsernameAlarm(false);
					} else {
						console.log("this username is NOT okay");
						setVerifyUsername(false);
						setVerifyUsernameAlarm(true);
					}
				});
		} else {
			setVerifyUsername(false);
			setVerifyUsernameAlarm(true);
		}
	}
	const checkPasswordsHandler = () => {
		if (user.password === user.password2) {
			setVeriftPasswords(true);
		} else {
			setVeriftPasswords(false);
		}
	};
	const logoutHandler = () => {
		sessionStorage.removeItem("userInfo");
		dispatch(userActions.user_logout());
	};

	return (
		<div id='Profile'>
			{updateMessage && (
				<Message variant='success'>
					{!verifyEmail && <li>this Email is taken</li>}
					{!verifyUsername && <li>this Username is taken</li>}
					{!verifypasswords && <li>passwords must match</li>}
				</Message>
			)}
			{updated && { logoutHandler }}

			<br />

			<Container>
				<Row className=' p-4'>
					<Col>
						<h2 className='p-4'>User Profile</h2>
						<Form className='p-4 rounded'>
							<Form.Group className='mb-3' controlId='formBasicEmail'>
								<Form.Label className='text-dark'>Email</Form.Label>
								<Form.Control
									onChange={handleChange}
									name='email'
									type='email'
									placeholder={userInfo.email}
								/>
								{verifyEmailAlarm && (
									<Form.Text className='text-muted'>
										<p className='text-dark'>
											<span className='text-danger'>
												<i className='fas fa-times-circle'></i>
											</span>
											This Email Is Not Valid
										</p>
									</Form.Text>
								)}
								{verifyEmail && (
									<Form.Text className='text-muted'>
										<p className='text-dark'>
											<span className='text-success'>
												<i className='fas fa-check-circle'></i>
											</span>
											Okay
										</p>
									</Form.Text>
								)}
								{/* <Form.Text className='text-muted'>
									<ul className=' text-dark'>
										<li>
											Please Enter Valid and Unique Email, this email
											validated after submit
										</li>
										<li>you can change it after validation.</li>
									</ul>
								</Form.Text> */}
							</Form.Group>
							<Form.Group className='mb-3' controlId='formBasicUsername'>
								<Form.Label className='text-dark'>Username</Form.Label>
								<Form.Control
									onFocus={checkEmailHandler}
									onChange={handleChange}
									name='username'
									type='text'
									placeholder={userInfo.username}
								/>
								{verifyUsernameAlarm && (
									<Form.Text className='text-muted'>
										<p className='text-dark'>
											<span className='text-danger'>
												<i className='fas fa-times-circle'></i>
											</span>
											This Username Is Not Valid
										</p>
									</Form.Text>
								)}
								{verifyUsername && (
									<Form.Text className='text-muted'>
										<p className='text-dark'>
											<span className='text-success'>
												<i className='fas fa-check-circle'></i>
											</span>
											Okay
										</p>
									</Form.Text>
								)}
								{/* <Form.Text className='text-muted'>
									<ul className=' text-dark'>
										<li>
											Please Enter Readable and Unique username.
										</li>
										<li>
											you can change it hardly after validation.
										</li>
									</ul>
								</Form.Text> */}
							</Form.Group>
							<Form.Group
								className='mb-3'
								controlId='formBasicFirstName'
							>
								<Form.Label className='text-dark'>
									First name
								</Form.Label>
								<Form.Control
									onFocus={checkUsernameHandler}
									onChange={handleChange}
									name='first_name'
									type='text'
									placeholder={userInfo.first_name}
								/>
							</Form.Group>
							<Form.Group className='mb-3' controlId='formBasicLastName'>
								<Form.Label className='text-dark'>Last name</Form.Label>
								<Form.Control
									onChange={handleChange}
									name='last_name'
									type='text'
									placeholder={userInfo.last_name}
								/>
							</Form.Group>

							<Form.Group className='mb-3' controlId='formBasicPassword'>
								<Form.Label className='text-daRK'>Password</Form.Label>
								<Form.Control
									onChange={handleChange}
									name='password'
									type='password'
									placeholder='Password'
								/>
								{/* <Form.Text className='text-muted'>
									<ul className=' text-dark'>
										<li>Please Dont use regular passwords.</li>
										<li>Dont use Predictable passwords.</li>
										<li>
											It must Containg Capitals and Regulars and
											Numbers And signs
											<ul>
												<li>numbers : 1234567890</li>
												<li>Capitals : ABCDEFGH....</li>
												<li>Signs : !@#$%^*()_+...</li>
											</ul>
										</li>
									</ul>
								</Form.Text> */}
							</Form.Group>
							<Form.Group
								className='mb-3'
								controlId='formBasicPassword2'
							>
								<Form.Label className='text-dark'>
									Password again
								</Form.Label>
								<Form.Control
									onFocus={checkPasswordsHandler}
									onChange={handleChange}
									name='password2'
									type='password'
									placeholder=' Re Enter Password'
								/>
								{!verifypasswords && user.password2.length !== 0 && (
									<Form.Text className='text-muted'>
										<p className='text-dark'>
											<span className='text-danger'>
												<i className='fas fa-times-circle'></i>
											</span>
											Passwords Not Match
										</p>
									</Form.Text>
								)}
								{verifypasswords && user.password2.length !== 0 && (
									<Form.Text className='text-muted'>
										<p className='text-dark'>
											<span className='text-success'>
												<i className='fas fa-check-circle'></i>
											</span>
											Okay
										</p>
									</Form.Text>
								)}
								{/* <Form.Text className='text-muted'>
									<ul className=' text-dark'>
										<li>Passwords must match</li>
									</ul>
								</Form.Text> */}
							</Form.Group>

							<Button
								onClick={UpdateProfileHandler}
								variant='success'
								type='button'
							>
								Update Account
							</Button>
						</Form>
					</Col>
					<Col>
						<h2 className='p-4'>Orders</h2>
					</Col>
				</Row>
			</Container>
		</div>
	);
}

export default DashBoard;
