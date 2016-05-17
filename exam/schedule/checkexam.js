var superagent = require('superagent');
var message = require('../models/message');

function updateExam(){
    superagent.get('http://gd.122.gov.cn/m/examplan/getExamPlanDetail')     //GET the Json of exam data 
    .query({
        fzjg: "%E7%B2%A4X",
        kskm: 3,
        ksdd: 440604,
        kscx: "C1",
        startTime: "2016-05-1",
        endTime: "2017-05-11",
        zt : 0,
    })
    .set('Accept', 'application/json')
    .end(function (err, data) {
        var datalist = data.body["data"];
        datalist.forEach(function (e) {
            message.find({}).remove().exec(function (err) {     //delete all old message in mongoDB
                var tt = new message({
                    kcmc: e["kcmc"],
                    ksrq: e["ksrq"],
                    kscc: e["kscc"],
                    kkrs: e["kkrs"]
                });
                tt.save(function (err) {                        //insert the latest message into mongoDB
                    if (err) {
                        console.log(err);
                    }
                });
            });
        });
        console.log("update well")
    })
}

module.exports = updateExam;