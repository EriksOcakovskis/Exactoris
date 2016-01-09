// Helpers
var url = window.location;
$('ul.nav a[href="'+ url +'"]').parent().addClass('active');
$('ul.nav a').filter(function() {
    return this.href == url;
}).parent().addClass('active');

function JobDoneAutoDate() {
  var checkbox = document.getElementById('job_done');
  var jobDoneDate = document.getElementById('job_done_date');
  var isodateNow = new Date().toISOString();
  var dateNow = new Date();
  var my_year = dateNow.getFullYear();
  var my_month = ('0'+(dateNow.getMonth() + 1)).slice(-2);
  var my_day = ('0'+dateNow.getDate()).slice(-2);
  var my_hours = ('0'+dateNow.getHours()).slice(-2);
  var my_minutes = ('0'+dateNow.getMinutes()).slice(-2);
  var my_seconds = ('0'+dateNow.getSeconds()).slice(-2);
  var newDate = my_year+"-"+my_month+"-"+my_day+" "+my_hours+":"+my_minutes+":"+my_seconds;

  if (checkbox.checked == true)
  {
    jobDoneDate.value = newDate.toString();
  }
  else
  {
    jobDoneDate.value = "";
  };
};

var userMenu = document.getElementById("id_work_assigned_to")
var jobStartDate = document.getElementById("id_start_date")
var isodateNow = new Date().toISOString();
var dateNow = new Date();
var my_year = dateNow.getFullYear();
var my_month = ('0'+(dateNow.getMonth() + 1)).slice(-2);
var my_day = ('0'+dateNow.getDate()).slice(-2);
var my_hours = ('0'+dateNow.getHours()).slice(-2);
var my_minutes = ('0'+dateNow.getMinutes()).slice(-2);
var my_seconds = ('0'+dateNow.getSeconds()).slice(-2);
var newDate = my_year+"-"+my_month+"-"+my_day+" "+my_hours+":"+my_minutes+":"+my_seconds;

// userMenu.onchange=function(){ //run some code when "onchange" event fires
//  var chosenoption=this.options[this.selectedIndex] //this refers to "selectmenu"
//  if (chosenoption.value!="nothing"){
//   jobStartDate.value = newDate.toString();
//  }
// }

// Copyright 2014-2015 Twitter, Inc.
// Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
  var msViewportStyle = document.createElement('style')
  msViewportStyle.appendChild(
    document.createTextNode(
      '@-ms-viewport{width:auto!important}'
    )
  )
  document.querySelector('head').appendChild(msViewportStyle)
}

// Date picker initializer
$(document).ready(function () {
    $(".datepicker").datetimepicker({
      format: 'DD.MM.YYYY',
      showTodayButton: true,
      showClear: true,
      useCurrent: false,
      keyBinds: { right: '', left: ''  }
    });
});

// Datetime picker initializer
$(document).ready(function () {
    $(".datetimepicker").datetimepicker({
      format: 'DD.MM.YYYY HH:mm:ss',
      showTodayButton: true,
      showClear: true,
      useCurrent: false,
      keyBinds: { right: '', left: ''  }
    });
});
