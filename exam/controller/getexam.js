var mongoose = require('mongoose');
var message = require('../models/message');
//find message from mongoDB and render a html 
function getexam(res){
    message.find({},function (err, dataset) {
        if (err) {
            return console.log(err);
        }
        else {
            console.log(dataset);
        }
        res.render('test', { data: dataset })
    });
}

module.exports = getexam;