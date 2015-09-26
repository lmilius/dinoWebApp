
$.ajax({
url:'/',
method:'GET',
type:'json',
headers:{'request':'Storeinfo'},
success:function(data){
console.log(data)
data=JSON.parse(data);
console.log(data)
src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"
for (var i in data) {
  console.log(data[i])
  var id = data[i][0];
  var name = data[i][2];
  var Quantity = data[i][3]
  var price= data[i][1]
  var txid= data[i][4]
  var element = document.getElementById("img-container");
  var str = "<form method='POST' id='999' action='http://pay.team9.isucdc.com/begin_transaction'><div class=relative>"  +'<img  src='+name+'>' + "<div class=text>"+id+"</p>"
  if(Quantity>0){
    str+="<div class=Quantity  >"+"Amount Remaining:"+Quantity+"</div>"
    str+="<div class=PriceIn  >"+"Price:"+price+"</div>"
     str+='<input type="submit"  id=play_button  '
  str+=';" value="Buy" />'+"</div>";
str+=' <input type="hidden" name="txid" value='+txid+ ' >'
str+= '<input type="hidden" name="postback"  value="dino.team9.isucdc.com/receipt">'
str+='<input type="hidden" name="amount" value='+price+' >'
  }
  else{
    str+="<div class=soldOut>"+'Sold Out'+"</div>"
        str+="<div class=PriceOut  >"+"Price:"+price+"</div>"
        str+='<input type="hidden"  id=play_button  '
  str+=';" value="Buy" />'+"</div>";
str+=' <input type="hidden" name="txid" value='+txid+ ' >'
str+= '<input type="hidden" name="postback"  value="dino.team9.isucdc.com/receipt">'
str+='<input type="hidden" name="amount" value='+price+' >'
  }


    element.innerHTML += str;
}}
});
