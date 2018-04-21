var express = require('express');
var router = express.Router();
var ObjectId = require('mongodb').ObjectId;

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/dbdata', function(req, res) {
  var db = req.db;
  var collection = db.get('seats');
  console.log(req.body);
  var today = new Date();
  var curtime = String(today);
  collection.insert(
    {
      space: req.body.space,
      nOfSeats: req.body.nOfSeats,
      nOfPeople: req.body.nOfPeople,
      time: curtime
    },
    function(err, docs) {
      if (err === null) {
        console.log(docs._id);
        res.json({ _id: docs._id });
      } else {
        console.log('fail');
        res.json({
          status: 'fail'
        });
      }
    }
  );
});

module.exports = router;
