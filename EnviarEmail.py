import smtplib
from pathlib import Path
from  email.message import EmailMessage

caminho = Path()
def enviar_email(title, file):
    TitleEmail = """
    <p> HISTORICO 10X/<p>
    <p> Segue o arquivo/<p>
    """
    emails = ['theusaguilar2@gmail.com', 'dhiegod18@gmail.com']
    msg = EmailMessage()
    msg['Subject' ] = title
    msg['From'] = 'theusaguilar2@gmail.com'
    msg['To'] = ','.join(emails)
    password = 'mzxjzhvqzdkbogie'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(TitleEmail)

    with open(f"{caminho}/{file}", "rb") as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file)   
    
    
    try:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password) 
        for destinatario  in emails:
            s.sendmail(msg['From'], destinatario,  msg.as_string().encode('utf-8'))
        s.quit()
    except: 
        return   

