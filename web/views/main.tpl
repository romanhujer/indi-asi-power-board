<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="60; URL=/main">
  <link rel="stylesheet" href="static/my.css" >
</head>

<title>PWR Manager</title>
</head>

<body bgcolor='#26262A'>
<div class='t'>
<table width='100%%'><tr><td><b><font size='5'>
PWR  web manager</font></b></td><td align='right'>
</td></tr>
</table>
</div >
<div class='b'>
<br />
<div style='width: 40em;'>
&nbsp;&nbsp;Time:<font class='c'><span id='datetime'></span></font> 
<script> 
function pad(num, size) { var s = '000000000' + num; return s.substr(s.length-size); }
var now = new Date(); 
          document.getElementById('datetime').innerHTML = (now.getMonth()+1)+'/'
          +pad(now.getDate().toString(),2)+'/'
          +pad(now.getFullYear().toString().substr(-2),2)+ ' '
          +pad(now.getHours().toString(),2)+':'
          +pad(now.getMinutes().toString(),2)+':'
          +pad(now.getSeconds().toString(),2); 
</script>
<br />
<br />
<br />
<table width='100%%'>

<tr><td>
<form action="/main" method="POST">
<input type="hidden"  name="id" value="p1">
PORT 1:<td><font class='c'>{{pt1}}</font><td><input class="slider" type="range" min="0" max="100" 
value={{pt1}} id="npt1" name="npt1"><td>&nbsp;
<td><font class='c'><span id="opt1"></span></font>
<td>&nbsp;<td><input type="submit" value="SET">
</form>
<tr><td>
<form action="/main" method="POST">
<input type="hidden"  name="id" value="p2">
PORT 2 <td><font class='c'>{{pt2}}</font><td><input class="slider" type="range" min="0" max="100" 
value={{pt2}} id="npt2" name="npt2"><td>&nbsp;
<td><font class='c'><span id="opt2"></span></font>
<td>&nbsp;<td><input type="submit" value="SET">
</form>
<tr><td>
<form action="/main" method="POST">
<input type="hidden" name="id" value="p3">
PORT 3:<td><font class='c'>{{pt3}}</font><td><input class="slider" type="range" min="0" max="100" 
value={{pt3}} id="npt3" name="npt3"><td>&nbsp;
<td><font class='c'><span id="opt3"></span></font>
<td>&nbsp;<td><input type="submit" value="SET">
</form>
<tr><td>
<form action="/main" method="POST">
<input type="hidden" name="id" value="p4">
PORT 4:<td><font class='c'>{{pt4}}</font><td><input class="slider" type="range" min="0" max="100" 
value={{pt4}} id="npt4" name="npt4"><td>&nbsp;
<td><font class='c'><span id="opt4"></span></font>
<td>&nbsp;<td><input type="submit" value="SET">
</form>
</table> 
</div>
<br />

<script>
var slider1 = document.getElementById("npt1");
var output1 = document.getElementById("opt1");
output1.innerHTML = slider1.value;
slider1.oninput = function() {
  output1.innerHTML = this.value;
}
</script>
<script>
var slider2 = document.getElementById("npt2");
var output2 = document.getElementById("opt2");
output2.innerHTML = slider2.value;
slider2.oninput = function() {
  output2.innerHTML = this.value;
}
</script>
<script>
var slider3 = document.getElementById("npt3");
var output3 = document.getElementById("opt3");
output3.innerHTML = slider3.value;
slider3.oninput = function() {
  output3.innerHTML = this.value;
}
</script>
<script>
var slider4 = document.getElementById("npt4");
var output4 = document.getElementById("opt4");
output4.innerHTML = slider4.value;
slider4.oninput = function() {
  output4.innerHTML = this.value;
}
</script>

</body>
</html>
