

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
function addNewInfo(){
alert('test');
var str='<form id="NewInfo">Headers: <input type="text" name="headers"><br> Text:<input type="text" name="info"></form>';
str+="<button onclick='sumbitInfo()'>Submit</button>";
document.getElementById("div2").innerHTML=str

}
function sumbitInfo(){
var json={'Headers':document.getElementById("NewInfo").elements['headers'].value,'Text':document.getElementById("NewInfo").elements['info'].value};
$.ajax({
url:'/',
method:'POST',
type:'json',
headers:{'request':'Newinfo'},
data:json

});
}
