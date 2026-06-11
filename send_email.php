<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

require 'PHPMailer/Exception.php';
require 'PHPMailer/PHPMailer.php';
require 'PHPMailer/SMTP.php';

$logFile = __DIR__ . '/mail_debug.log';
file_put_contents($logFile, "Script started at ".date('Y-m-d H:i:s')."\n", FILE_APPEND);

$mail = new PHPMailer(true);

try {
    // SMTP Configuration for MailHog
    $mail->isSMTP();
    $mail->Host = 'localhost';
    $mail->Port = 1025;
    $mail->SMTPAuth = false;  // No authentication needed
    
    // Debug settings
    $mail->SMTPDebug = SMTP::DEBUG_CONNECTION;
    $mail->Debugoutput = function($str, $level) use ($logFile) {
        file_put_contents($logFile, "$level: $str\n", FILE_APPEND);
    };

    // Email content
    $mail->setFrom('brac.arup@gmail.com', 'Localhost Test');
    $mail->addAddress('brac.arup@gmail.com');
    $mail->Subject = 'Test from MAMP Localhost';
    $mail->Body = 'This email was sent from MAMP localhost!';

    $mail->send();
    file_put_contents($logFile, "Email sent successfully!\n", FILE_APPEND);
    echo "Email captured by MailHog! View at: http://localhost:8025";
} catch (Exception $e) {
    $error = "Mailer Error: " . $e->getMessage() . "\n";
    file_put_contents($logFile, $error, FILE_APPEND);
    die($error);
}