# -*- coding: utf-8 -*-
# Python libraries that we need to import for our bot
import os
import random

from flask import Flask, request
from pymessenger.bot import Bot

from ConnectionDatabase import ConnectionDatabase as conn
from UsersServices import UsersServices as check


app = Flask(__name__)

ACCESS_TOKEN = 'EAAFUPy2BT5cBAGt8EoEdgQH2TjaDVdi2v7SUAivZCOA78Lo4PCImN2oXComjzAkxUgtU8V7p29TWkcu4mJ9ntrB4YplZCszo2T4CLNH322QAvSM1Vi4zerk4D7UfrZBaJRzpV7Vnd7BZC6hmY3bwgGd7GbqJ3STIcUSW4uGtFgZDZD'
VERIFY_TOKEN = 'PYFYTOKENAPI'
ID_BOT = 112495156767265
DATABASE = 'PYFY.db'
TABLE = 'users'
bot = Bot(ACCESS_TOKEN)

list_user = []

## Variaveis de base
step1 = '0.0'
step1_2 = '0.1'
step2 = '0.2'
step3 = '0.3'
step4 = '1.0'
step5 = '2.0'
step6 = '3.0'


## Lista de perguntas
list_questions  = {
'1': 'Qual sua idade?',
'2': 'Como você se sente atualmente?',
'3': 'Sente-se agitado ultimamente?',
'4': 'Anda fazendo muitas atividades ultimamente?',
'5': 'Anda focando muito a sua atenção para algo que não dava importância antes?',
'6': 'Tem tomado decisões sem pensar nos resultados?',
'7': 'Se sente com muita energia no corpo?',
'8': 'Tem problemas em se concentrar?',
'9': 'Fica ansioso quando não tem algo para fazer?',
'10': 'Perde o interesse nas coisas que faz no dia a dia?',
'11': 'Tem sido otimista nos últimos dias?',
'12': 'Anda sem vontade de fazer as coisas do dia a dia?',
'13': 'Se sente sem valor , ou que não se encaixa no mundo?',
'14': 'É excessivamente crítico consigo mesmo?',
'15': 'Reclama muito das coisas?',
'16': 'Não sente mais vontade de sair ou fazer coisas divertidas?',
'17': 'Se sente triste?',
'18': 'Esses sintomas aparecem em períodos específicos? Se sim qual?',
'19': 'Acha que descumpriu alguma promessa recentemente?',
'20': 'Ultimamente teve pouco interesse em fazer coisas que te interessam ou te dão prazer?',
'21': 'Ultimamente vem tendo dificuldade para dormir ou tem dormido mais que o costume?',
'22': 'Anda sem fome ultimamente?',
'23': 'Teve aumento no seu apetite recentemente?',
'24': 'Se sente lento para se mover ou falar ao ponto de alguém a sua volta perceber?',
'25': 'Já sofreu ou sofre de algum tipo mau trato?',
'26': 'Já foi ou é alvo de bullying?',
'27': 'Tem vontade de machucar a si mesmo?',
'28': 'Se sente alguns desses sintomas acima, a quanto tempo vem sentindo?',
}


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        entry = output.get('entry')[0]
        messaging = entry.get('messaging')[0]
        sender = messaging.get('sender').get('id')
        id_sender = int(sender)

        if ID_BOT != id_sender:
            if 'message' in messaging:
                text = str(messaging.get('message').get("text", ""))

                if checkBase(id_sender):
                    if check('').getStep(id_sender).__eq__(step2):
                        print('Fazer Cadastro')
                        startStep(step2, id_sender, text)

                    elif check('').getStep(id_sender).__eq__(step3):
                        print('Valida Nome')
                        startStep(step3, id_sender, text)

                    elif check('').getStep(id_sender).__contains__('1.'):
                        if not check('').getStep(id_sender).__eq__('1.29'):
                            print('perguntas')
                            startStep(step4, id_sender, text)
                        else:
                            print('challenges p')

                    elif check('').getStep(id_sender).__eq__(step5):
                        print('Seq Pergunta')
                        startStep(step5, id_sender, text)

                    else:
                        print('challenges')

                else:
                    print('Primeira vez')
                    startStep(step1, id_sender, '')

            else:
                print("Sem Message")

    return "Message Processed"


# chooses a random message to send to the user
def get_message():
    sample_responses = ["Você esta bem?", "Bem vindo!", "Eu sou a PyFy", "Converse comigo, gosto de aprender :)"]
    # return selected item to the user
    return random.choice(sample_responses)


def get_picture():
    IMG = '..\\files\\rick.jpeg'
    sample_responses = ["Você esta bem?", "Bem vindo!", "Eu sou a PyFy", "Converse comigo, gosto de aprender :)"]
    # return selected item to the user
    return random.choice(IMG)


def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def checkBase(id):
    return check('').checkExist(id)


def checkQuestion(id, text):
    connec = conn(DATABASE)
    if check('').getStep(id).__eq__('1.1'):
        quest = "'" + text + "'"
        connec.updateQuestions(TABLE, id, quest)
        connec.updateStep(TABLE, id, '1.2')
        send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.2'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        send_message(id, '\'S\' para Sim, \'N\' para Não ou \'A\' para As vezes')
        send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.18'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.28'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        send_message(id, 'Obrigado Por responder o questionario!')
        send_message(id, 'Caso tenha alguma dúvida deseja indicar alguma melhoria, ou queira fazer alguma alteração dos seus dados, por favor entre em contato no e-mail: pyfy@gmail.com')
        send_message(id, 'Iremos analisar as respostas enviadas e entraremos em contato em breve!')

    else:
        if text.upper().__eq__('S'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))
        elif text.upper().__eq__('N'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))
        elif text.upper().__eq__('A'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))
        else:
            send_message(id, 'Opcao invalida, tente novamente!')
            send_message(id, '\'S\' para Sim, \'N\' para Não ou \'A\' para As vezes')
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))


def getNextQuestion(id):
    next = '1.' + str(float(check('').getStep(id)[2:]) + 1).replace('.0','')
    return "'"+next+"'"


def getQuest(id, text):
    return "'" + check('').getQuestions(id) + ';' + text + "'"


def startStep(step, id, text):
    connec = conn(DATABASE)

    begin = step.__eq__(step1)
    beginName = step.__eq__(step1_2)
    pre_registration = step.__eq__(step2)
    validate_registration = step.__eq__(step3)
    questions = step.__eq__(step4)
    validate_questions = step.__eq__(step5)
    challenges = step.__eq__(step6)

    if begin:
        connec.insert(TABLE, id, '', 0.2, '')
        send_message(id, 'Bem vindo ao PYFY!\nO nosso objetivo é ajudar pessoas através de uma metodologia desenvolvida para identificar sintomas de depressao, para que possamos auxiliar a buscar pelo tratamento')
        send_message(id, 'Por gentileza informe o seu nome')
    elif beginName:
        send_message(id, 'Por gentileza informe o seu nome')
    elif pre_registration:
        connec.updateName(TABLE, id, "'"+text+"'")
        send_message(id, f'{text}, Seu Nome esta correto? - \'S\' Sim e \'N\' Não')
        connec.updateStep(TABLE, id, 0.3)
    elif validate_registration:
        if text.upper().__eq__('S'):
            send_message(id, 'Correto!')
            send_message(id, f'Bem vindo {connec.formatter(check.getName(id))}')
            send_message(id, 'A nossa metodologia foi desenvolvida através de serie de perguntas, poderiamos começar? - \'S\' Sim e \'N\' Não')
            connec.updateStep(TABLE, id, 2.0)
        elif text.upper().__eq__('N'):
            send_message(id, 'Por gentileza informe o seu nome')
            connec.updateStep(TABLE, id, 0.2)
        else:
            send_message(id, 'Opcao invalida, tente novamente!')
            send_message(id, f'{connec.formatter(check.getName(id))}, Seu Nome esta correto? - \'S\' Sim e \'N\' Não')
    elif questions:
        checkQuestion(id, text)

    elif validate_questions:
        if text.upper().__eq__('S'):
            # Realizar primera pergunta
            send_message(id, list_questions.get('1'))
            connec.updateStep(TABLE, id, 1.1)
        elif text.upper().__eq__('N'):
            send_message(id, 'Obrigado pela oportunidade!')
            connec.updateStep(TABLE, id, 3.0)
        else:
            send_message(id, 'Opcao invalida, tente novamente!')
            send_message(id, 'Você gostaria de responder um questionario? - \'S\' Sim e \'N\' Não')

    elif challenges:
        send_message(id, 'Diga que voce é lindo!')
    else:
        send_message(id, 'NOT FOUND')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
