


       

<?php 

//print_r($teploty);

?>

<table>
<caption style="text-decoration: underline;padding-bottom: 10px">Nastavení programu Voda </caption>

<?php 

echo form_open("termostat/submit_voda");
echo "\n";
for ($i = 0 ; $i < 2 ; $i++)
{
    
    echo "<tr>";
    echo "<td>";
    echo "Start "; echo  ($i + 1); echo ":";
    echo "</td>";
    echo "<td>";         
    $s["type"] = "time";
    $s["step"] = "any";
    $s["name"] = sprintf("start %d",$teploty[$i]->number);
    $s["value"] = $teploty[$i]->start;
    $s["style"] = "width:100px";
    $s["id"] = $s["name"];
    $s["class"] = "formik";
    echo form_input($s);
    echo "</td>";
    echo "</tr>\n";
    
    echo "<tr>";
    echo "<td>";
    echo "Stop "; echo  ($i + 1); echo ":";
    echo "</td>";
    echo "<td>";
    $s["type"] = "time";
    $s["step"] = "any";
    $s["name"] = sprintf("stop %d",$teploty[$i]->number);
    $s["value"] = $teploty[$i]->stop;
    $s["id"] = $s["name"];
    echo form_input($s);    
    echo "</td>";
    echo "</tr>\n";
}
?>

<tr><td>Maximální <br> teplota vody: </td> <td> 
<?php 
$s["type"] = "number";
$s["step"] = "0.5";
$s["name"] = "teplota";
$s["value"] = $teploty[0]->teplota;    
$s["min"]= "0";

echo form_input($s);
?>
</td>
</tr>

<tr> <td colspan="2">
<br>
<?php 
$s["type"] = "submit";
$s["name"] = "submit";
$s["value"] = "Uložit změny";
$s["id"] = "submita";
$s["style"]= "width: 100%";
//echo form_submit('submit', 'Změnit nastavení', 'id="submita"');
echo form_submit($s);
echo form_close();
?>
</td>

</tr>
</table>


</script>

    


