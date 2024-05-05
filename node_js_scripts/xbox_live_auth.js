#!/usr/bin/env node
const { authenticate } = require('@xboxreplay/xboxlive-auth');

// Import the dotenv package
const dotenv = require('dotenv');

// Load the environment variables from the .env file
dotenv.config();

// Assign environment variables to variables
const username = process.env.USERNAME;
const password = process.env.PASSWORD;

authenticate(username, password,)
	.then(console.info)
	.catch(console.error);


// authenticate(username, password, { raw: true })
//     .then(console.info)
//     .catch(console.error);












// const { live } = '@xboxreplay/xboxlive-auth';

// // Import the dotenv package
// const dotenv = require('dotenv');

// // Load the environment variables from the .env file
// dotenv.config();

// // Assign environment variables to variables
// const client_id = process.env.CLIENT_ID;
// const redirect_uri = process.env.REDIRECT_URI;


// const authorizeUrl = live.getAuthorizeUrl(
// 	client_id,
// 	'XboxLive.signin XboxLive.offline_access',
// 	'code',
// 	redirect_uri
// );

// console.info(authorizeUrl);