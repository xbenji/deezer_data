<?php
	
	function displayChart($table, $key) {
		
		//connect
		$m = new MongoClient();
		$db = $m->deezer_charts;
		$collection = $db->selectCollection($table);
		
		// get elements matching query
		$query = array( 'key' => $key );	
		$result = $collection->find($query);

		// iterate through the results
		foreach ($result as $item) {
			foreach ($item["charts"] as $song) {
				echo $song["song"] . "\t" . $song["count"] . "\n";		
			}
		}
	}

?>