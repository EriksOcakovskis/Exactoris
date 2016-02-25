// Helpers
var url = window.location;
$('ul.nav a[href="'+ url +'"]').parent().addClass('active');
$('ul.nav a').filter(function() {
    return this.href == url;
}).parent().addClass('active');

function clearValue(el_id) {
  var el_id = document.getElementById(el_id)
  el_id.value = '';
}

// Hack, it is not pretty, you will regert making it
function overflowHack() {
  var anim_cont = document.getElementById('animation_container');
  ac = window.getComputedStyle(anim_cont, null)
  if (ac.height == '52.5px') {
    anim_cont.style.overflow = 'visible'
  }else {
    clearValue('id_typeof_recurrence')
    clearValue('id_dateof_recurrence')
  }
}

// Animator
function animate(options) {

  var start = new Date();

  var id = setInterval(function() {
    timePassed = new Date() - start
    progress = timePassed / options.duration

    if (progress > 1) {progress = 1};

    var delta = options.delta(progress)
    options.step(delta)

    if (progress == 1) {
      clearInterval(id)
      overflowHack()
    };

  }, options.delay || 10)
}

// Anumation properties for height change
function changeHeight(element, delta, duration) {
  var to = 52.5;

  animate({
    delay: 20,
    duration: duration || 1000,
    delta: delta || function(e) {return e},
    step: function (delta) {
      element.style.height = to*delta + 'px'
    }
  });
}

// Recurrence show/hide script
function showHideRecurrence(){
  var checkbox = document.getElementById('recurring');
  var anim_cont = document.getElementById('animation_container');

  if (checkbox.checked == true) {
    changeHeight(anim_cont, '',200)
  } else{
    anim_cont.style.overflow = 'hidden'
    changeHeight(anim_cont, function(e) {return 1-e}, 200)
  };
}

//
var checkbox = document.getElementById('recurring');
if (checkbox) {
  if (checkbox.checked == true) {
  var anim_cont = document.getElementById('animation_container');
  anim_cont.style.height = '52.5px'
  }
}


function JobDoneAutoDate(){
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
