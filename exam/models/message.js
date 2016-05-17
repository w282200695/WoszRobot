var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/test');

var message = mongoose.model("message", {
    kcmc: String,
    ksrq: String,
    kscc: String,
    kkrs: Number
});

module.exports = message;