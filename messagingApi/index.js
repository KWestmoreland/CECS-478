const express = require('express');
const routes = require('./api/routes/api')

// set up express app
const app = express();

// initialize routes
app.use('/tasks', routes);

// listen for requests
app.listen(process.env.port || 3000, function(){
	console.log('now listening for requests');
});

