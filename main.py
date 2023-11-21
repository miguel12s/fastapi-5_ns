
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app= FastAPI()

origins=[
    "https://fastapi-dyl9-production.up.railway.app/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
class EmailItem(BaseModel):
    subject: str
    message: str
    to_email: str

@app.post("/send-email/")
def send_email(item: EmailItem):
    # Configura la conexión SMTP para Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "miguelaspet@gmail.com"  # Reemplaza con tu dirección de correo electrónico de Gmail
    smtp_password = "xrldipesfbgzmbag"  # Reemplaza con tu contraseña de aplicación generada

    # Configura el mensaje de correo
    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = item.to_email
    msg["Subject"] = item.subject

    # Agrega el cuerpo del mensaje
    msg.attach(MIMEText(item.message, "plain"))

    try:
        # Inicia la conexión SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Inicia la sesión SMTP
            server.starttls()

            # Inicia sesión con las credenciales
            server.login(smtp_username, smtp_password)

            # Envía el correo
            server.sendmail(smtp_username, item.to_email, msg.as_string())

        return {"message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")