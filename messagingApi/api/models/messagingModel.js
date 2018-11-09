'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

//Create schema for messages 
var MessageSchema = new Schema({
  name: {
    type: String,
    //required: 'Kindly enter the name of the task'
    required: [true, 'Please enter a name']
  },
  message: {
    type: String
  },
  Message_date: {
    type: Date,
    default: Date.now
  },
});

//Create schema for Users
var UserSchema = new Schema({
  name: {
    type: String,
    required: [true, 'Please enter a name']
  },
  password: {
    type: String,
    required: [true, 'Please enter a password']
  },
});

module.exports = mongoose.model('Messages', MessageSchema);
module.exports = mongoose.model('MyUsers', UserSchema);
