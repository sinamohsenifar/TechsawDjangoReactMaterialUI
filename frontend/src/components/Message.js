import React from "react";
import { Alert } from "react-bootstrap";

export default function Message({ variant, children }) {
	return (
		<Alert variant={variant}>
			<span className='text-light'>
				<ul>{children}</ul>
			</span>
		</Alert>
	);
}
