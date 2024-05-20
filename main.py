import openai
import pandas as pd
import smtplib
from email.mime.text import MIMEText

openai.api_key = 'APIkey'

def lire_donnees_csv(fichier_csv):
    return pd.read_csv(fichier_csv)

def generer_email(personne):
    prompt = (
        f"Rédigez un email formel de la part de l'équipe de {personne['entreprise']} à {personne['prénom']} {personne['nom']} dans la langue suivante :{personne['langue']} , "
        f"lui demandant de cliquer sur l'URL suivante : {personne['URL']}. "
        f"L'email doit être professionnel, poli, et indiquer qu'il s'agit d'une communication importante de la part de {personne['entreprise']}."
    )

    #requête à l'API GPT
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    message_content = chat_completion.choices[0].message.content.strip()
    return message_content

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

subject = "Important"

sender = "infop296@gmail.com"
password = "password"


def main():
    fichier_csv = 'data.csv'
    donnees = lire_donnees_csv(fichier_csv)
    
    # Générer et afficher les emails pour chaque personne
    for index, personne in donnees.iterrows():
        email = generer_email(personne)
        recipient = personne['email']
        if isinstance(recipient, str) and '@' in recipient:
            email_body = generer_email(personne)
            send_email(subject, email_body, sender, recipient, password)
        else:
            print(f"Invalid email for {personne['prénom']} {personne['nom']}: {recipient}")
        
if __name__ == '__main__':
    main()
