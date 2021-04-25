# froma de enviar correos desde  python
from email.mime.text import MIMEText
import smtplib
# MIME = Multi-purpose Internet Mail Extensions
from email.mime.multipart import MIMEMultipart

mensaje = MIMEMultipart()
password = '1234567890cueva'
mensaje['From'] = 'jcueva12380@gmail.com' # cliente del correo
mensaje['subject'] = 'Registro completado!'

def enviarCorreo(para, nombre):
    mensaje['To'] = para # el correo a quien quiero enviar el correo
    cuerpo = 'Hola! {} \n Gracias por comunicarte conmigo, nos pondremos en contacto pronto! 👽👽😁'.format(nombre)
    mensaje.attach(MIMEText(cuerpo, 'plain')) #ahora, adjunto toda la configuracion del correo con el cuerpo del mensaje a enviar  le indico en que formato se mandará
    try:
        servidorSMTP = smtplib.SMTP('smtp.gmail.com', 587)
        #configuro mi servidor smtp (que va a ser el encargado de conectarse con los servidores de outlook)
        servidorSMTP.starttls() #indico que el metodo cifrado del envio de los correo sea starttls
        servidorSMTP.login(mensaje['From'], password)
        servidorSMTP.sendmail(
            mensaje['From'],
            mensaje['To'],
            mensaje.as_string()
        )# envio el correo con toda la configuracion del mensaje previeamente realizada
        servidorSMTP.quit() #me desconecto porque sino la proxima vez que vuelva a hacer login puede generar conflictos de autenticaión
        return True
    except Exception as e:
        print(e)
        return False
