<?php
function str_containsV2($haystack, $needle) {
	return $needle !== '' && strpos($haystack, $needle) !== false; 
}

$url = base64_decode($_GET['url']);

$ar = true;

$hdrs = [];
foreach (json_decode(base64_decode($_GET['headers']), true) as $name => $value) {
    if ($name == "X-PHPProxy-AllowRedirects") {
        if ($value == "false") {
            $ar = false;
        }
        continue;
    }
    $hdrs[] = "$name: $value";
}


$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);


if ($ar) {
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
}

curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $hdrs);


$response = curl_exec($ch);
$header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
$header = substr($response, 0, $header_size);
$body = substr($response, $header_size);
curl_close ($ch);


foreach(explode("\n", $header) as $h) {
    if (str_containsV2($h, "HTTP")) {continue;};
    header($h);
}


echo $body;
?>