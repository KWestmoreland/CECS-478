'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

//Create schema for messages 
var MessageSchema = new Schema({
  sender: {
    type: String,
    required: [true, 'Please enter a sender']
  },
  receiver: {
    type: String,
    required: [true, 'Please enter a receiver']
  },
  message: {
    type: String,
    required: [true, 'Please enter a message']
  },
  Message_date: {
    type: Date,
    default: Date.now
  },
  status: {
    type: String,
    default: 'New'
  },
  sender_ID: {
    type: String,
    default: 'None'
  },
});

//Create schema for Users
var UserSchema = new Schema({
  name: {
    type: String,
    required: [true, 'Please enter a name'],
    unique: [true, 'This name is already in use']
  },
  password: {
    type: String,
    required: [true, 'Please enter a password']
  },
});

//var UserSchema = new Schema({
 // name

module.exports = mongoose.model('Messages', MessageSchema);
module.exports = mongoose.model('MyUsers', UserSchema);
