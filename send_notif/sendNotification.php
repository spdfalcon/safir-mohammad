<?php
require_once '../../../includes/db_config.php';

// Ensure the content type is JSON
header('Content-Type: application/json');
$response = array();
// Get the JSON data sent via POST
$postData = file_get_contents("php://input");
$jsonData = json_decode($postData, true);

if (!empty($jsonData) && isset($jsonData['title']) && isset($jsonData['content'])) {
        $title = $jsonData['title'];
        $message = $jsonData['content'];

        // Your Firebase Cloud Messaging server key
        $serverKey = 'AAAA73hWHS4:APA91bHEHQtVPlNTnx6QHT3wctjxGm3S1yGCpVpMWL5YMSwMGZIzpLks-8cG5Jh0A9BxA-xhbiqDNcdq4L_VfCCIGpcdtLQNFn9o8db3vERdeMnNpHmpFJm1Bm7KKXk2Dbse0DVzoigF';

        // Combined payload
        $payload = [
            'to' => '/topics/user',
            'priority' => 'high',
            'notification' => [
                'title' => $title,
                'body' => $message
            ]
        ];

        // Initialize cURL
        $ch = curl_init('https://fcm.googleapis.com/fcm/send');

        // Set headers and cURL options
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Authorization: key=' . $serverKey
            ],
            CURLOPT_POSTFIELDS => json_encode($payload)
        ]);

        // Execute cURL request
        $responseBody = curl_exec($ch);

        // Check if the request was successful
        if ($responseBody === false) {
            $response['success'] = false;
            $response['message'] = "error please try again!";
        } else {
            $response['success'] = true;
            $response['message'] = "Notification sent successfully";
        }

        // Close cURL session
        curl_close($ch);
    } else {
        $response['success'] = false;
        $response['message'] = "error please try again!";
    }

echo json_encode($response);

?>
