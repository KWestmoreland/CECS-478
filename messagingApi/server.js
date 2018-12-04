var express = require('express'),
  app = express(), //set up express app
  port = process.env.PORT || 3000,
  mongoose = require('mongoose'),
  Message = require('./api/models/messagingModel'), //created model loading here
  bodyParser = require('body-parser'),
  jwt = require('jsonwebtoken');
  
// mongoose instance connection url connection
mongoose.Promise = global.Promise; //Possibly causing deprecated message
mongoose.connect('mongodb://localhost/test'); //creates location if missing

app.use(express.static('public'));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


var publicRoutes = require('./api/routes/public/publicRoutes'); //importing route
var privateRoutes = require('./api/routes/private/privateRoutes');
publicRoutes(app); //register the route
privateRoutes(app);


app.listen(port); //listen for requests


console.log('todo list RESTful API server started on: ' + port);

app.use(function(req, res) {
  res.status(404).send({url: req.originalUrl + ' not found'})
});

