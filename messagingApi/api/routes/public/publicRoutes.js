'use strict';
module.exports = function(app) {
  var messagingController = require('../../controllers/messagingController');

  app.route('/api/register')
    .post(messagingController.register);

 /* app.route('/api/users')
    .get(messagingController.list_all_users)
    .delete(messagingController.delete_all_users);*/

  app.route('/api/signin')
    .post(messagingController.signin);

  /*app.route('/api/delete')
    .delete(messagingController.delete_all_messages);*/
};
