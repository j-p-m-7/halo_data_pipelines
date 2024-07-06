#!/usr/bin/env node
const { authenticate } = require('@xboxreplay/xboxlive-auth');

// Import the dotenv package
const dotenv = require('dotenv');

// Load the environment variables from the .env file
dotenv.config();

// Assign environment variables to variables
const username = process.env.USERNAME;
const password = process.env.PASSWORD;

authenticate(username, password, { raw: true })
    .then(console.info)
    .catch(console.error);