var express = require('express');
var router = express.Router();
var ObjectId = require('mongodb').ObjectId;

router.get('/seats', function(req, res, next) {
  var db = req.db;
  var collection = db.get('seats');
  collection.find({}, {}, function(err, docs) {
    if (err === null) {
      res.json(docs);
    } else {
      res.send({
        msg: err
      });
    }
  });
});

module.exports = router;
