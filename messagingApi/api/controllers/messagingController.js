'use strict';


var mongoose = require('mongoose'),
  Message = mongoose.model('Messages'),
  User = mongoose.model('MyUsers');

var jwt = require('jsonwebtoken');
var app = require('express');
var config = require('../../config.js');
var bcrypt = require('bcryptjs');

//Shows all messages in DB
exports.list_all_messages = function(req, res) { 
  Message.find({}, function(err, message) {
    if (err)
      res.send(err);
    res.json(message); 
  });
};

//Lists all users in DB
exports.list_all_users = function(req, res) {
  User.find({}, function(err, user) {
    if (err)
      res.send(err);
    res.json(user);
  });
};

//Saves a new User in the DB
exports.register = function(req, res) { //POST Request
  var hashedPassword = bcrypt.hashSync(req.body.password, config.saltRounds);
  var new_user = new User({
    name : req.body.name,
    password : hashedPassword
  });
 
  console.log(req.body);

  new_user.save(function(err, user) {
    if (err) {
      res.status(422).send(err);
      console.log('User register error');
    }
    else
     res.json(user);
  });
};

//Authenticates an existing user by sending back a JWT if successful
exports.signin = function(req, res) {
  User.findOne({
    name: req.body.name
  },
  function(err, user) {
    if (err) {
      res.status(422).send(err);
    }
    if (!user) {
      res.json({ 
        success: false,
        message: 'Authentication failed. User not found.'
      });
    }
    else if (user) {
      //check if password matches
      if (!bcrypt.compareSync(req.body.password, user.password)) {
        res.json({
          success: false,
          message: 'Authentication failed. Wrong password.'
        });
      }
      else {
        //create a token with only our given payload
        const payload = {
          name: user.name
        };
        var token = jwt.sign(payload, config.secret, {
          expiresIn: 60*60*24 //24 hours
        });
       
        // return the information including token as JSON
        res.json({
          success: true,
          message: 'Enjoy your token',
          token: token,
          user_ID: user._id
        });
      }
    }
  });
};  

//Save a new message in the DB
exports.create_a_message = function(req, res) { //POST Request
  var new_message = new Message(req.body); //Creates new message model with request

  console.log(req.body); //Test show POST requests on console

  new_message.save(function(err, message) { //Saves to the database
    if (err){ //Error catching
      res.status(422).send(err);
      console.log('POST Error');}
    else
      res.json(message);
  });
};

//Reads a message and sends it back to requester
exports.read_a_message = function(req, res) { //GET request of a specific id
  Message.findById(req.params.messageId, function(err, message) {
    if (err)
      res.send(err);
    res.json(message);
  });
};

//Updates a message with the parameters on request
exports.update_a_message = function(req, res) {
 Message.findByIdAndUpdate({_id: req.params.messageId}, req.body, {new: true}).then(function(message){
    res.json(message);
 }); 
};

//Deletes a message of given ID
exports.delete_a_message = function(req, res) { //DELETE Request

//Finds a message by _id value and deletes them from the database
 Message.findByIdAndRemove({_id: req.params.messageId}).then(function(message){
   res.send(message);
 });
};
