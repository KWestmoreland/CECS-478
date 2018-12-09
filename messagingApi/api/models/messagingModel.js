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
  iv: {
    type: String,
    default: 'None'
  },
  signature: {
    type: String,
    default: 'None'
  },
  Message_date: {
    type: Date,
    default: Date.now
  },
  status: {
    type: String,
    default: 'New'
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
  DH_Pub_Key: {
    type: String,
    default: 'None'
  },
  Signed_DH_Pub_Key: {
    type: String,
    default: 'None'
  },
  RSA_Pub_Key: {
    type: String,
    default: 'None'
  },
});

//var UserSchema = new Schema({
 // name

module.exports = mongoose.model('Messages', MessageSchema);
module.exports = mongoose.model('MyUsers', UserSchema);
