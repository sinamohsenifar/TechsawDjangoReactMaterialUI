import React, { useState } from "react";
import { Container, Form, Button, Row, Col } from "react-bootstrap";
import { Navigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { userRegister } from "../store/usersAsyncAction";
import Message from "../components/Message";
import axiosInstance from "../axios";

function SignUpScreen() {
	// create refrences to get values from form
	// let emailInput = React.createRef();
	// let usernameInput = React.createRef();
	// let passwordInput = React.createRef();
	// let password2Input = React.createRef();

	// this is how we get refrences current values
	const [signUpMessage, setSignUpMessage] = useState(false);

	const userInfo = useSelector((state) => state.user);
	const dispatch = useDispatch();

	const [verifyEmail, setVerifyEmail] = useState(false);
	const [verifyUsername, setVerifyUsername] = useState(false);
	const [verifypasswords, setVeriftPasswords] = useState(false);

	const [verifyEmailAlarm, setVerifyEmailAlarm] = useState(false);
	const [verifyUsernameAlarm, setVerifyUsernameAlarm] = useState(false);

	const [user, setUser] = useState({
		username: "",
		email: "",
		password: "",
		password2: "",
	});
	const handleChange = (event) => {
		setUser({ ...user, [event.target.name]: event.target.value });
	};

	async function SignUpHandler() {
		if (user.password === user.password2 && verifyEmail && verifyUsername) {
			setSignUpMessage(false);
			dispatch(userRegister(user.email, user.username, user.password2));

			document.getElementById("formBasicEmail").value = "";
			document.getElementById("formBasicUsername").value = "";
			document.getElementById("formBasicPassword").value = "";
			document.getElementById("formBasicPassword2").value = "";

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
			setSignUpMessage(true);
		}
	}
	async function checkEmailHandler() {
		if (user.email.length > 7) {
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
		if (user.username.length >= 3) {
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

	return (
		<div id='RegisterForm'>
			{signUpMessage && (
				<Message variant='success'>
					{!verifyEmail && <li>this Email is taken</li>}
					{!verifyUsername && <li>this Username is taken</li>}
					{!verifypasswords && <li>passwords must match</li>}
				</Message>
			)}
			{userInfo.error.data && (
				<Message variant='danger'>
					{<li>userInfo.error.data.detail</li>}
				</Message>
			)}
			<br />
			{userInfo.user.refresh && <Navigate to='/' />}
			<Container>
				<Row className=' p-4'>
					<Col>
						<Form className='p-4 bg-info rounded'>
							<Form.Group className='mb-3' controlId='formBasicEmail'>
								<Form.Label className='text-light'>Email</Form.Label>
								<Form.Control
									onChange={handleChange}
									name='email'
									type='email'
									placeholder='Enter email'
								/>
								{verifyEmailAlarm && (
									<Form.Text className='text-muted'>
										<p className='text-light'>
											<span className='text-danger'>
												<i className='fas fa-times-circle'></i>
											</span>
											This Email Is Not Valid
										</p>
									</Form.Text>
								)}
								{verifyEmail && (
									<Form.Text className='text-muted'>
										<p className='text-light'>
											<span className='text-success'>
												<i className='fas fa-check-circle'></i>
											</span>
											Okay
										</p>
									</Form.Text>
								)}
								<Form.Text className='text-muted'>
									<ul className=' text-light'>
										<li>
											Please Enter Valid and Unique Email, this email
											validated after submit
										</li>
										<li>you can change it after validation.</li>
									</ul>
								</Form.Text>
							</Form.Group>
							<Form.Group className='mb-3' controlId='formBasicUsername'>
								<Form.Label className='text-light'>Username</Form.Label>
								<Form.Control
									onFocus={checkEmailHandler}
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
								<Form.Text className='text-muted'>
									<ul className=' text-light'>
										<li>
											Please Enter Readable and Unique username.
										</li>
										<li>
											you can change it hardly after validation.
										</li>
									</ul>
								</Form.Text>
							</Form.Group>
							<Form.Group className='mb-3' controlId='formBasicPassword'>
								<Form.Label className='text-light'>Password</Form.Label>
								<Form.Control
									onFocus={checkUsernameHandler}
									onChange={handleChange}
									name='password'
									type='password'
									placeholder='Password'
								/>
								<Form.Text className='text-muted'>
									<ul className=' text-light'>
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
								</Form.Text>
							</Form.Group>
							<Form.Group
								className='mb-3'
								controlId='formBasicPassword2'
							>
								<Form.Label className='text-light'>
									Type Password AGAIN
								</Form.Label>
								<Form.Control
									onFocus={checkPasswordsHandler}
									onChange={handleChange}
									name='password2'
									type='password'
									placeholder=' Re Enter Password'
								/>
								{!verifypasswords && (
									<Form.Text className='text-muted'>
										<p className='text-light'>
											<span className='text-danger'>
												<i className='fas fa-times-circle'></i>
											</span>
											Passwords Not Match
										</p>
									</Form.Text>
								)}
								{verifypasswords && (
									<Form.Text className='text-muted'>
										<p className='text-light'>
											<span className='text-success'>
												<i className='fas fa-check-circle'></i>
											</span>
											Okay
										</p>
									</Form.Text>
								)}
								<Form.Text className='text-muted'>
									<ul className=' text-light'>
										<li>Passwords must match</li>
									</ul>
								</Form.Text>
							</Form.Group>

							<Button
								onClick={SignUpHandler}
								variant='success'
								type='button'
							>
								Create Account
							</Button>
						</Form>
					</Col>
				</Row>
			</Container>
		</div>
	);
}

export default SignUpScreen;
