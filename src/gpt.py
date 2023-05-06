import os
import openai
# openai.organization = "org-swV3CkBYAGp9mVrsZvRAMK4H"
openai.api_key = "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"


import os
from twilio.rest import Client
import openai

#! API SSID: SKac9ba3d67f52decf5eb7c39a212b8e42
#! API SECRET: SKac9ba3d67f52decf5eb7c39a212b8e42

# Configurar as chaves de API
TWILIO_ACCOUNT_SID = 'ACf1eab61cf5542fdd55f07cb6b188da61'
TWILIO_AUTH_TOKEN = 'af77a4cc89978e0ffffbb68180521e2c'
OPENAI_API_KEY = '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'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai.api_key = OPENAI_API_KEY

def get_gpt_response(message):
    prompt = f"Pergunta: {message}\nResposta:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()



def process_message(body):
    # Obter a mensagem do corpo da solicitação
    message = body['Body']

    # Obter a resposta do ChatGPT
    response = get_gpt_response(message)

    # Enviar a resposta de volta para o remetente
    message = client.messages.create(
        body=response,
        from_='whatsapp:' + os.environ['TWILIO_PHONE_NUMBER'],
        to='whatsapp:' + body['From'],
    )

    print(f"Resposta enviada: {response}")


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Obter a solicitação do webhook do Twilio
    body = request.values

    # Processar a mensagem usando o ChatGPT
    process_message(body)

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()


# https://seu-dominio.com/webhook
