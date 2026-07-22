<?php
$pdo = new PDO('mysql:dbname=resonator;host=db', 'resonator-admin', '020707', [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);

$query = $pdo->query('SHOW VARIABLES like "version"');

$row = $query->fetch();

echo 'MySQL version:' . $row['Value'];

// nice it fucking works