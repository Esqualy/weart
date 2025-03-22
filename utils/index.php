<?php
// PORT 5000 => CDN.WE-ART.APP | PORT 8000 => WE-ART.APP
$flask_url = 'http://89.213.140.99:5000';

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $flask_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Exécuter la requête et obtenir la réponse
$response = curl_exec($ch);

// Vérifier si des erreurs se produisent lors de la requête cURL
if (curl_errno($ch)) {
    // En cas d'erreur, afficher l'erreur cURL
    echo 'Erreur cURL : ' . curl_error($ch);
} else {
    // Si la requête est réussie, afficher la réponse de l'application Flask
    echo 'Réponse de Flask : ' . $response;
}

// Fermer la session cURL
curl_close($ch);
?>
