import React from "react";
import ProductsList from "../components/products/ProductsList";
import { styled } from "@mui/material/styles";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import PhotoCamera from "@mui/icons-material/PhotoCamera";

const Input = styled("input")({
	display: "none",
});

export default function HomeScreen() {
	return (
		<React.Fragment>
			<Button
				color='success'
				variant='contained'
				onClick={() => {
					alert("Clicked!");
				}}
			>
				Button
			</Button>
			<Button
				color='error'
				variant='outlined'
				onClick={() => {
					alert("Clicked!");
				}}
			>
				Button
			</Button>
			<Button variant='outlined' disabled>
				Disabled
			</Button>

			<label htmlFor='contained-button-file'>
				<Input
					accept='image/*'
					id='contained-button-file'
					multiple
					type='file'
				/>
				<Button variant='contained' component='span'>
					Upload
				</Button>
			</label>
			<label htmlFor='icon-button-file'>
				<Input accept='image/*' id='icon-button-file' type='file' />
				<IconButton
					color='primary'
					aria-label='upload picture'
					component='span'
				>
					<PhotoCamera />
				</IconButton>
			</label>
			<ProductsList />
		</React.Fragment>
	);
}
