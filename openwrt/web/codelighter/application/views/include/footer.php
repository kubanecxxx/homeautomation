
<script type="text/javascript" charset="utf-8">
		$('input').click(function(){
			$(this).select();	
		});
	</script>

<div id="footer">
	
	<?php
$path = $this->config->item('root') . 'application/views/pages';
$map = directory_map($path);

// rint_r ($map);

echo '<ul id="header_items">';
foreach ($map as $row) {
    $row = str_replace('_content.php', '', $row);
    echo '<li id=header_item>';
    $coje = array(
        'm' => $row,
        'id' => 'a_header'
    );
    echo anchor('termostat/' . $row, str_replace('_', ' ', ucfirst($row)), $coje);
    echo '</li>';
}
echo '</ul>';
?>
</div>


</body>
</html>