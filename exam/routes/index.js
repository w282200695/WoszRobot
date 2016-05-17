var express = require('express');
var router = express.Router();
var getExam = require('../controller/getexam.js');

/* GET home page. */
router.get('/', function (req, res) {
    getExam(res);
});

router.get('/test', function (req, res){
    getExam(res);
})
module.exports = router;