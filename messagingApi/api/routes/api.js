const express = require('express');
const router = express.Router();

// get request
router.get('/tasks', function(req, res){
	res.send({type:'GET'});
});

// post request
router.post('/tasks', function(req, res){
        res.send({type:'POST'});
});

// update request
router.put('/tasks/:id', function(req, res){
        res.send({type:'PUT'});
});

// delete request
router.delete('/tasks/:id', function(req, res){
        res.send({type:'DELETE'});
});

module.export = router;

