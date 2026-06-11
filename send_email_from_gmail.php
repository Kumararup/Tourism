<?php
// send_email_from_gmail.php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

// Enable error reporting
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Use absolute paths
require __DIR__ . '/PHPMailer/Exception.php';
require __DIR__ . '/PHPMailer/PHPMailer.php';
require __DIR__ . '/PHPMailer/SMTP.php';

// Create log file
$logFile = __DIR__ . '/mail_debug.log';
file_put_contents($logFile, "WEB SCRIPT START: ".date('Y-m-d H:i:s')."\n", FILE_APPEND);

$mail = new PHPMailer(true);

try {
    // SMTP Configuration for Gmail
    $mail->isSMTP();
    $mail->Host = 'smtp.gmail.com';
    $mail->SMTPAuth = true;
    $mail->Username = 'brac.arup@gmail.com';
    $mail->Password = 'layi wgdg mhdl nyrw'; // Replace with your 16-digit app password
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail->Port = 587;
    
    // Debug settings
    $mail->SMTPDebug = SMTP::DEBUG_SERVER;
    $mail->Debugoutput = function($str, $level) use ($logFile) {
        file_put_contents($logFile, "$level: $str\n", FILE_APPEND);
    };

    // Email content
    $mail->setFrom('brac.arup@gmail.com', 'Web Test');
    $mail->addAddress('brac.arup@gmail.com');
    $mail->Subject = 'Test from Browser';
    $mail->Body = 'This email was sent from a browser request!';

    $mail->send();
    file_put_contents($logFile, "WEB: Email sent successfully!\n", FILE_APPEND);
    echo "Email sent successfully from browser!";
} catch (Exception $e) {
    $error = "WEB Mailer Error: " . $e->getMessage();
    file_put_contents($logFile, $error, FILE_APPEND);
    die($error);
}