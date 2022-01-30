import React, { useEffect } from "react";
import { Navigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { userActions } from "../store/store";

function LogoutComponent() {
	const userInfo = useSelector((state) => state.user);
	const dispatch = useDispatch();

	async function logout() {
		dispatch(userActions.user_logout());
	}

	useEffect(() => {
		logout();
	});
	return <div>{!userInfo.loginStatus && <Navigate to='/login/' />}</div>;
}

export default LogoutComponent;
