import Footer from "./components/Footer";
import Header from "./components/Header";
import { Container } from "react-bootstrap";
import HomeScreen from "./screens/HomeScreen";
import ProductScreen from "./screens/ProductScreen";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import React from "react";
import CartScreen from "./screens/CartScreen";
import SignUpScreen from "./screens/SignUpScreen";
import LoginScreen from "./screens/LoginScreen";
import DashBoard from "./screens/DashBoard";
import LogoutComponent from "./components/LogoutComponent";

function App() {
	return (
		<BrowserRouter>
			<Header />
			<Container className='main'>
				<Routes>
					<Route exact path='/' element={<HomeScreen />} />
					<Route exact path='product/:id' element={<ProductScreen />} />
					<Route exact path='login/' element={<LoginScreen />} />
					{/* <Route exact path='logout/' element={<LogoutComponent />} /> */}
					<Route exact path='signup/' element={<SignUpScreen />} />
					<Route exact path='dashboard/' element={<DashBoard />} />
					<Route exact path='cart/' element={<CartScreen />} />
					<Route exact path='cart/:id' element={<CartScreen />} />
				</Routes>
			</Container>
			<Footer />
		</BrowserRouter>
	);
}

export default App;
