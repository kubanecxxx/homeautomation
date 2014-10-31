


       

<?php 

//print_r($teploty);

?>


<table>
<caption style="text-decoration: underline;padding-bottom: 10px">Nastavení programu topení</caption>

<?php 

echo validation_errors();
echo form_open("termostat/submit_heating");
echo "\n";

$cha[0] = "Týden";
$cha[1] = "<br>Víkend";

$b = 0;

for ($j = 0 ; $j < count($rows) ; $j++)
{         
    $m = sprintf ("<tr>  <td>%s</td>    <td></td>    <td></td>    </tr>",$cha[$j]);
    echo $m;
    $table = $rows[$j];
    
    $start = 0;
    $offset = $j * 100;
    
    ?>
    <tr><td>Start</td><td>Stop</td><td>Teplota</td></tr>
    <?php 
    
    for ($i = 0 ; $i < count($table) ; $i++)
    {
        $d = $table[$i];
        echo "<tr>\n\t";    
        
        echo "<td>";
        //start time
        $s["type"] = "time";
        $s["step"] = "any";
        $s["name"] = $b++;
        $s["value"] = $d->start;
        $s["style"] = "width: 80px";
        $s["class"] = "formik";
        $s["id"] = sprintf("start%d",$offset + $start++);
        unset ($s["disabled"]);

        echo form_input($s);
        
        unset($s["class"]);
        echo "</td>\n\t";
        
        
        echo "<td>";
        //stop time
        $s["value"] = $d->stop;
        $s["disabled"] = 1;
        
        
        $temp = $start % count($table);
        
        $s["id"] = sprintf("stop%d",$offset + $temp );        
        echo form_input($s);
        unset($s["id"]);
        echo "</td>\n\t";
        
        
        echo "<td>";
        //temperature
        $s["type"] = "number";
        $s["step"] = 0.5;
        $s["min"] = 0;
        $s["name"] = $b++;
        $s["value"] = $d->teplota;
        unset ($s["disabled"]);
        echo form_input($s);
        echo "</td>\n";
        echo "</tr>\n";
    }    
    
}
?>


</td>
</tr>

<tr> <td colspan = 3>
<br>
<?php 
$s["type"] = "submit";
$s["name"] = "submit";
$s["value"] = "Uložit změny";
$s["id"] = "submita";
$s["style"]= "width: 100%";
echo form_submit($s);
echo form_close();
?>
</td>

</tr>
</table>



<script type="text/javascript">

function pushLimits()
{
	var i;
	var ja = 4;
	for (i = 0; i < ja; i++)
	{
		var obj = $('#start' + i);
		var post = $('#start' + (i + 1) % ja);
		var pre =  $('#start' + (i + ja -1) % ja);
		obj.attr("min",pre.val());
		obj.attr("max",post.val());
		$("div.ji").append(obj.val() + post.val() + pre.val() + "<br>");
	}
};


$(document).ready( function(){

	//pushLimits();
})


$(".formik").change(function(event)
	{
	    var t = event.target.id;
	    t = t.replace("start","stop");
	    var obj = $('#' + t);
    	obj.val(event.target.value);
    	//pushLimits();
	});



</script>


