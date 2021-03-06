/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = PsiTurk(uniqueId, adServerLoc);

var myassignment;

$.ajax({
  dataType: "json",
  url: "/get_condition",
  success: function (data) {
  	myassignment = data.condition; // load the next few stims from the server
  }
});

// All pages to be loaded
var pages = [
	"instructions/instruct-ready.html",
	"stage.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
	"instructions/instruct-ready.html"
];


var Drawing = function() {
	
	psiTurk.showPage('stage.html');

	d3.select('#image')
	  .append("img")
	  .attr("src",myassignment.filename)
	  .attr("height",myassignment.height)
	  .attr("width",myassignment.width);



	var sketchpad = Raphael.sketchpad("editor", {
		width: myassignment.width,
		height: myassignment.height,  // set these based on tile size
		editing: true
	});


	var pen = sketchpad.pen();
	pen.width(2);

	
	d3.select('#editor')
		.attr("height", myassignment.height)
		.attr("width", myassignment.width);

	$("#widthslider").rangeslider({
	    // Feature detection
	    polyfill: true
	});

 	$(document).on('change', "#widthslider", function(e) {
        var value = e.target.value;
        pen.width(value);
    });

	$("#colorslider").rangeslider({
	    // Feature detection
	    polyfill: true
	});

 	$(document).on('change', "#colorslider", function(e) {
        var value = parseInt(e.target.value);
        var hexcode = value.toString(16);
        pen.color("#"+hexcode+hexcode+hexcode);
    });


	prompt_resubmit = function() {
		replaceBody(error_message);
		$("#resubmit").click(resubmit);
	};

	resubmit = function() {
		replaceBody("<h1>Trying to resubmit...</h1>");
		reprompt = setTimeout(prompt_resubmit, 10000);
		
		psiTurk.saveData({
			success: function() {
			    clearInterval(reprompt); 
                            psiTurk.computeBonus('compute_bonus', function(){finish()}); 
			}, 
			error: prompt_resubmit}
		);
	};

	$('#Undo').click(function() {
		sketchpad.undo();
	});

	$('#StartOver').click(function() {
		sketchpad.clear();
	});


	savetile = function(filename, drawing_data) {
		sendData = {"filename": filename,
				"drawing_data": drawing_data};
		$.ajax({
		  dataType: "json",
		  type: "POST",
		  url: "/complete_condition",
		  data: sendData,
		  success: function (data) {
		  	psiTurk.completeHIT(); 
		  }
		});
	}


	$('#Next').click(function() {
		drawing_data = sketchpad.json(); 
		psiTurk.recordUnstructuredData("drawing_json", drawing_data);
	    psiTurk.saveData({
            success: function(){ 
            	savetile(myassignment.filename, drawing_data)
            }, 
            error: prompt_resubmit
        });
	});

};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){

    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { currentview = new Drawing(); } // what you want to do when you are done with instructions
    );
});
