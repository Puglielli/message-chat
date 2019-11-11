# Python libraries that we need to import for our bot
import os
import random
from flask import Flask, request
from pymessenger.bot import Bot

from src.services.ConnectionDatabase import ConnectionDatabase as conn
from src.services.UsersServices import UsersServices as check

app = Flask(__name__)
ACCESS_TOKEN = 'EAAFUPy2BT5cBAGt8EoEdgQH2TjaDVdi2v7SUAivZCOA78Lo4PCImN2oXComjzAkxUgtU8V7p29TWkcu4mJ9ntrB4YplZCszo2T4CLNH322QAvSM1Vi4zerk4D7UfrZBaJRzpV7Vnd7BZC6hmY3bwgGd7GbqJ3STIcUSW4uGtFgZDZD'
VERIFY_TOKEN = 'PYFYTOKENAPI'
ID_BOT = 112495156767265
DATABASE = 'db_files/PYFY.db'
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

        # if event.get('message').get('text'):
        #     print("Messenge: " + str(event.get('message').get('text')))

        # for event in output['entry']:
        #     messaging = event['messaging']
        #
        #     for message in messaging:
        #         if message.get('message'):
        #             print("ID: " + str(message['sender']['id']) + ", Messagem: " + str(message['sender']))
        #             # Facebook Messenger ID for user so we know where to send response back to
        #             recipient_id = message['sender']['id']
        #             #print("Data User" + str(message['sender']))
        #             if message['message'].get('text'):
        #                 #print(message['message'].get('text'))
        #                 response_sent_text = get_message()
        #                 if (recipient_id == "2239164186181399"):
        #                     send_message(recipient_id, "Olá Samuel Seu GostoSÃO")
        #                 elif (recipient_id == "2345448712228712"):
        #                     send_message(recipient_id, "Seja Bem vindo Samuel!")
        #                 else:
        #                     send_message(recipient_id, response_sent_text)
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


connec = conn(DATABASE)


# def checkRegister(step):
#     begin = step.__eq__(step1)
#     pre_registration = step.__eq__(step2)
#
#     if begin or pre_registration:
#         return True
#     else:
#         return False


def checkBase(id):
    return check('').checkExist(id)


def checkQuestion(step, id, text):
    if check('').getStep(id).__eq__('1.1'):
        quest = "'" + text + "'"
        connec.updateQuestions(TABLE, id, quest)
        connec.updateStep(TABLE, id, '1.2')
        send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.2'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        send_message(id, '\'S\' Sim, \'N\' Não ou \'T\' Talvez')
        send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.18'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.28'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        send_message(id, 'Obrigado Por responder o questionario')

    else:
        if text.upper().__eq__('S'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))
        elif text.upper().__eq__('N'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))
        elif text.upper().__eq__('T'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))
        else:
            send_message(id, 'Opcao invalida, tente novamente!')
            send_message(id, '\'S\' Sim, \'N\' Não ou \'T\' Talvez')
            send_message(id, list_questions.get(str(int(check('').getStep(id)[2:]))))


def getNextQuestion(id):
    next = '1.' + str(float(check('').getStep(id)[2:]) + 1).replace('.0','')
    return "'"+next+"'"


def getQuest(id, text):
    return "'" + check('').getQuestions(id) + ';' + text + "'"



def startStep(step, id, text):
    begin = step.__eq__(step1)
    beginName = step.__eq__(step1_2)
    pre_registration = step.__eq__(step2)
    validate_registration = step.__eq__(step3)
    questions = step.__eq__(step4)
    validate_questions = step.__eq__(step5)
    challenges = step.__eq__(step6)

    if begin:
        connec.insert(TABLE, id, '', 0.2, '')
        send_message(id, 'Bem vindo ao PYFY - Nos temos o objetivo de...')
        send_message(id, 'Informe Seu Primeiro Nome?')
    elif beginName:
        send_message(id, 'Informe Seu Primeiro Nome?')
    elif pre_registration:
        connec.updateName(TABLE, id, "'"+text+"'")
        send_message(id, f'{text}, Seu Nome esta correto? - \'S\' Sim e \'N\' Não')
        connec.updateStep(TABLE, id, 0.3)
    elif validate_registration:
        if text.upper().__eq__('S'):
            send_message(id, 'Correto!')
            send_message(id, f'Bem vindo {connec.formatter(check.getName(id))}')
            send_message(id, 'Você gostaria de responder um questionario? - \'S\' Sim e \'N\' Não')
            connec.updateStep(TABLE, id, 2.0)
        elif text.upper().__eq__('N'):
            send_message(id, 'Informe Seu Primeiro Nome?')
            connec.updateStep(TABLE, id, 0.2)
        else:
            send_message(id, 'Opcao invalida, tente novamente!')
            send_message(id, f'{connec.formatter(check.getName(id))}, Seu Nome esta correto? - \'S\' Sim e \'N\' Não')
    elif questions:
        checkQuestion(step, id, text)

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


# def insert(id_sender, name, date):
#     conn = ConnectionDatabase(DATABASE)
#     conn.insert(id_sender, name, date)
#
#
# def isExist(id_user):
#     conn = ConnectionDatabase(DATABASE)
#     if conn.getName(id_user).__contains__("[]"):
#         return False
#     else:
#         return True
#
#
# def getName(id_user):
#     conn = ConnectionDatabase(DATABASE)
#     return conn.formatter(conn.getName(id_user))
#
#
# def insertUser(id, name, choice):
#     global list_user
#     data = {}
#     data['id'] = id
#     data['name'] = name
#     data['choice'] = choice
#     size = len(list_user)
#     list_user.insert(size, data)
#
#
# def getUser(id):
#     global list_user
#     size = len(list_user)
#     data = {}
#     data['id'] = 0
#     data['name'] = 'default'
#     data['choice'] = 'Z'
#     lista = data
#     for i in range(size):
#         idTemp = list_user[i].get('id')
#         if id == idTemp:
#             lista = list_user[i]
#         else:
#             continue
#     return lista
#
#
#
# def updateUser(id, name):
#     global list_user
#     size = len(list_user)
#     for i in range(size):
#         idTemp = list_user[i].get('id')
#         if id == idTemp:
#             list_user[i]['name'] = name
#
#
# def deleteUser(id):
#     global list_user
#     data = getUser(id)
#     if data.get('id') != 0:
#         list_user.remove(data)
#
#
# def getDate():
#     return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
