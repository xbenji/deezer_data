<?php

	header("Content-Type: text/plain");

	include 'utils.php';
	displayChart("country_charts", $_GET['country']);

?>
