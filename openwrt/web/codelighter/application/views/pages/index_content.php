
<script type="text/javascript"
	src="<?php echo base_url();?>application/views/fire-0.62.min.js"></script>

<script>

function showing(){
	
   var id = $('select#programy').val();

   var t = $('select#programy option:selected').attr('temperature');
   $('input#zadanaTeplota').attr('value',t);
   
   if (id == 1)
   {
   	$('input#zadanaTeplota').removeAttr("disabled");
       $('input#zadanaTeplota').show();
       
   }
   else if ( id == 3)
   {
   	$('input#zadanaTeplota').show();
   	$('input#zadanaTeplota').attr("disabled","disabled");
   }
   else
   {
   	$('input#zadanaTeplota').hide();
   	$('input#zadanaTeplota').attr("disabled","disabled");
   }
	
}

	   var topit = <?php Print($topit);?>
	   //var topit = 1

	$(document).ready( function(){
		showing();

		$('.fire').fire({
			speed:80,
			maxPow:7,
			gravity:2,
			flameWidth:3,
			flameHeight:0,
			plasm:false,
			fireTransparency:37,
			fadingFlameSpeed:8,
			mouseEffect:true,
			burnBorders:false,
			yOffset:-100,
			maxPowZone:'center'
		});	

		if (topit)
		{
			$('.fire').fire('play');
		}
		else
		{
			$('.fire').fire('stop');
		}

		
		
	});

    </script>




<?php $arr = $teploty; ?>


<table>
	<caption style="text-decoration: underline; padding-bottom: 10px">Hlavní
		nabídka</caption>
	<tr>

		<td>
<?php

// rint_r($teploty);
// echo $this->table->generate($teploty->result_array());
$attr = array(
    'class' => 'program',
    'id' => 'myform'
);
echo form_open("termostat/submit_program", $attr);

echo form_dropdown_kuba('programy', $programy, $program->id, "id=programy class=jupi");
?>

</td>
		<td>
<?php echo form_submit('submit', 'Zvolit program', 'id="submita" class="jupi"');?>


</td>
	</tr>
	<tr>
		<td><?php
$a["name"] = "teplota";
$a["value"] = "0.0";
$a["type"] = "number";
$a["id"] = "zadanaTeplota";
$a["min"] = "0";
$a["step"] = "0.5";
$a["class"] = "jupi";
echo form_input($a);
?>
<?php


echo form_close();
?>

</td>
		<td></td>
	</tr>
	<tr>
		<td>
 
 <?php echo $this->termometer->getImg($arr->home,False,15,1, "id=nevim"); ?>
    </td>
		<td>
<?php echo $this->termometer->getImg($arr->water,True,25,2, "id=nevim "); ?>
</td>

	</tr>
	<tr>
		<td></td>
		<td style>
<?php
if ($zije->event == 0)
    echo "nefungujeme od " . $zije->cas;
?>	
	</td>
	</tr>
</table>



<div id=divNeco class=fire></div>


<div class="moje"></div>


<script type="text/javascript">
/*
$('#submita').click(function() {
        var program_id = $('#programy').val();
        var temp = $('#zadanaTeplota').val();
        
        var form_data = {
                programy : program_id,
                teplota: temp,
                ajax: '1'
        };

        $.ajax({
                url: "<?php echo site_url('termostat/submit_program'); ?>",
                type: 'POST',
                data: form_data,
                success: function(msg) {
                    $('#main_content').html(msg);
                	
                }
        });
                
        return false;
});
*/
$('select#programy').change(showing);

var timer = null;

function goAway() {
    clearTimeout(timer);
    timer = setTimeout(function() {
    	 location.href = location.href;
    }, 30000);
}

window.addEventListener('mousemove', goAway, true);

goAway();  // start the first timer off

</script>

