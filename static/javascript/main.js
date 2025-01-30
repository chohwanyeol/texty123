
window.onload=function() {
 document.getElementById("preview").onclick=processText;
}

function processText() {
 var txtBox = document.getElementsByClassName("input");
 var lines = txtBox.value.split("\n");

 // generate HTML version of text
 var resultString  = "<p>";
 for (var i = 0; i < lines.length; i++) {
   resultString += lines[i] + "<br />";
 }
 resultString += "</p>";

 // print out to page
 var   blk   = document.getElementsByClassName("output");
 blk.innerHTML  =  resultString; 
}