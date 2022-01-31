<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
%if not running :
  <meta http-equiv="refresh" content="15; URL=/dslr">
%else:
  <meta http-equiv="refresh" content="2; URL=/dslr">
%end
  <link rel="stylesheet" href="static/my.css" >
</head>

<title>ASI-PWR-Manager</title>
</head>

<body bgcolor='#26262A'>
<div class='t'>
<table width='100%%'><tr><td><b><font size='5'>
DSLR Timer</font></b></td><td align='right'>
</td></tr>
</table>
</div >
<div class='b'>
<br />
<div style='width: 40em;'>
<span id='datetime'></span>
%if running :
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font class='c'><b>Timer is running</b> </font>
%end
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
<table width='100%'>
<tr>
%if not running :
  <tr>
  <form action="/dslr" method="POST">
  <input type="hidden" name="id" value="timer">
  <td width=140>Exposure count 
  <td width=10>:<td><font class='c'><input type="number" min=1 max=999  name="icount" value="{{count}}"</input></font>
  <tr>
  <td>Duration (sec.)
  <td>:<td><font class='c'><input type="number" min=1 max=3600 name="iexptime" value="{{exptime}}"</input></font>
  <tr>
  <td>Delay (sec.)
  <td>:<td> <font class='c'><input type="number" min=1 max=3600 name="iwait" value="{{wait}}"</input></font>
  <tr>
  <td>&nbsp;
  <tr>
  <td><td>
  <td><input type="submit" value="Start">
  </form>
%else:
  <tr>
  <td width=140>Exposure number<td width=10>:<td width=70><font class='c'><b>{{i_count}}</b></font><td width=20>of<td width=10>:<td>{{count}}
  <tr> 
  <td>Duratino (sec.)<td>:<td><font class='c'><b>{{i_exptime}}</b></font><td>of<td>:<td>{{exptime}} 
  <tr>
  <td>Delay(sec.)<td>:<td><font class='c'><b>{{i_wait}}</b></font><td>of<td>:<td>{{wait}}  
  <tr>
  <td>&nbsp; 
  <tr>
  <td>&nbsp;
  <tr> 
  <td><td><td>
   <form action="/dslr" method="POST">
        <input type="hidden" name="id" value="stop">
        <input type="submit" value="STOP">
   </form>
%end
</table> 
</div>
<br />
<br />
<br />
%if dslr == 'N' :
<a href='/main'>Home</a> 
%end
%if running :
<a href='/dslr'>Refresh</a>
%end
</body>
</html>

