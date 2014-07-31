
<script type="text/javascript"
	src="<?php echo base_url();?>application/views/fire-0.62.min.js"></script>

<script>
<?php //echo $topit; ?>




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

	$(document).ready( function(){
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

		showing();
		
	});

    </script>

<div id=divCenter class=fire></div>

<div id=divCenter>
       



<?php $arr = $teploty->result(); ?>


<table>
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

echo form_dropdown_kuba('programy', $programy, $program->id, 'id="programy"');
?>

</td><td>
<?php echo form_submit('submit', 'Zvolit program', 'id="submita"');?>

<?php echo form_close();
?>
</td>
</tr>
<tr>
<td><?php echo form_input('zadanaTeplota', 0, 'id="zadanaTeplota"');?></td>
<td></td>
		</tr>
		<tr>
			<td>
 
 <?php echo $this->termometer->getImg($arr[0]->value,False, "id=nevim"); ?>
    </td>
			<td>
<?php echo $this->termometer->getImg($arr[1]->value,True, "id=nevim"); ?>
</td>

		</tr>
	</table>

</div>

<div class="moje"></div>


<script type="text/javascript">
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

$('select#programy').change(showing);

var timer = null;

function goAway() {
    clearTimeout(timer);
    timer = setTimeout(function() {
    	 location.href = location.href;
    }, 3000);
}

window.addEventListener('mousemove', goAway, true);

goAway();  // start the first timer off

</script>

