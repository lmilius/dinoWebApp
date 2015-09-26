src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"
$.ajax({
url:'/',
method:'GET',
type:'json',
headers:{'request':'receipt','orderID':getParameterByName('orderID')},
success:function(data){
data=data.toString().replace('[','').replace('[','');
data=data.split(',');
console.log(data);



  var id = data[0];
  var money = data[1];
  var purchased=data[2];
  var PurchaseProf=data[3]
  var element = document.getElementById("img-container");

  if (data == null){}
    var str = '<p>Thank you for buying this item<p> <p> Your purchase id is '+ id  + "<p>The amount paid is :"+ money+'<p> The item has been purchased:'+purchased+'<p>The proof of pruchase is :'+ PurchaseProf;

    element.innerHTML += str;
  } else {
    var str = '<p>ACCESS DENIED<p>';

    element.innerHTML += str;
  }

},
error:function(error){
console.log(error);
console.log('error');


}
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
};
