'use strict';
module.exports = function(app) {
  var messagingController = require('../../controllers/messagingController');
  var verifyToken = require('../../../verifyToken');

  // todoList Routes
  app.route('/messages')
    .get(verifyToken, messagingController.list_all_messages)
    .post(verifyToken, messagingController.create_a_message);


  app.route('/message/:messageId')
    .get(verifyToken, messagingController.read_a_message)
    .put(verifyToken, messagingController.update_a_message)
    .delete(verifyToken, messagingController.delete_a_message);

};
