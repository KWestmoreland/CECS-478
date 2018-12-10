'use strict';
module.exports = function(app) {
  var messagingController = require('../../controllers/messagingController');
  var verifyToken = require('../../../verifyToken');

  // todoList Routes
  app.route('/allmessages')
    .get(verifyToken, messagingController.list_all_messages)

  app.route('/messages')
    .post(verifyToken, messagingController.create_a_message);

  app.route('/message/:messageId')
    .get(verifyToken, messagingController.read_a_message)
    .put(verifyToken, messagingController.update_a_message)
    .delete(verifyToken, messagingController.delete_a_message);

  app.route('/messages/:receiver')
    .get(verifyToken, messagingController.read_new_messages);

  app.route('/messages/new/:receiver')
    .get(verifyToken, messagingController.read_new_unread_messages);

  app.route('/messages/sent/:sender')
    .get(verifyToken, messagingController.read_sent_messages);

  app.route('/api/users/:username')
    .get(verifyToken, messagingController.retrieve_public_keys);


 // app.route('/contacts/:userID')
   // .get(verifyToken, messagingController.list_contacts)
   // .post(verifyToken, messagingController.create_a_contact);
   // .put(verifyToken, messagingController.update_a_contact)
   // .delete(verifyToken, messagingController.delete_a_contact);
};
