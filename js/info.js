

src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"
$.ajax({
url:'/',
method:'GET',
type:'json',
headers:{'request':'info'},
success:function(data){

json=JSON.parse(data);
for (var i in json) {


  var id = json[i][0];
  var info = json[i][1];
  var element = document.getElementById("img-container");
  var str = "<div class=relative>" + "<div class=HeaderInfo>" + id + "</p>"
  str += "<div class=textInfo>" + info + "</p>"

  element.innerHTML += str;}

}
});
