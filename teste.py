# -*- coding: utf-8 -*-
from datetime import datetime
from ConnectionDatabase import ConnectionDatabase as conn
from UsersServices import UsersServices as check

DATABASE = 'PYFY.db'
TABLE = 'users'
list_user = []


dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)


def insertUser(id, name, choice):
    global list_user
    data = {}
    data['id'] = id
    data['name'] = name
    data['choice'] = choice
    size = len(list_user)
    list_user.insert(size, data)


def getUser(id):
    global list_user
    size = len(list_user)
    data = {}
    data['id'] = 0
    data['name'] = 'default'
    data['choice'] = 'Z'
    lista = data
    for i in range(size):
        idTemp = list_user[i].get('id')
        if id == idTemp:
            lista = list_user[i]
        else:
            continue
    return lista



def updateUser(id, name):
    global list_user
    size = len(list_user)
    for i in range(size):
        idTemp = list_user[i].get('id')
        if id == idTemp:
            list_user[i]['name'] = name


def deleteUser(id):
    global list_user
    data = getUser(id)
    if data.get('id') != 0:
        list_user.remove(data)

#
# insertUser(12345, 'Philip', 'S')
# insertUser(123456, 'Pedrt', 'N')
# print("Size: " + str(len(list_user)))
# print(list_user[0])
# print(list_user[1])
#
#
# print(getUser(123456).get('name'))
# updateUser(123456, 'Samuel')
# print(getUser(123456).get('name'))
# print(list_user[1])
#
# print(getUser(123456).get('choice') == 'N')
#
# insertUser(12345678,'','N')
#
# print(list_user)
#
# deleteUser(1)
#
# print("Novos")
# print(list_user)
# # print(list_user[1])
# print(getUser(1).get('id') != 0)

#
# def getDate():
#     return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#
# if id2 in list_user:
#     print(list_user)
#     list_user.remove(id)
#     print(list_user)
# else:
#     choice = input('S ou N')
#     if choice == 'S':
#         print(list_user)
#         list_user.remove(id)
#         print(list_user) newstep = getNextQuestion(id)
#
#

connec = conn(DATABASE)
# connec.create(TABLE)
# connec.insert(BASE, 2, 'Paula', 0.0)
# connec.updateStep(BASE, 1, 0.0)
print(connec.getAll(TABLE))
#conn.close()



## Variaveis de base
step1 = '0.0'
step1_2 = '0.1'
step2 = '0.2'
step3 = '0.3'
step4 = '1.0'
step5 = '2.0'
step6 = '3.0'



## Lista de perguntas
list_questions = {
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
        print('Bem vindo ao PYFY - Nos temos o objetivo de...')
        print('Informe Seu Primeiro Nome?')
    elif beginName:
        print('Informe Seu Primeiro Nome?')
    elif pre_registration:
        connec.updateName(TABLE, id, "'"+text+"'")
        print(f'{text}, Seu Nome esta correto? - \'S\' Sim e \'N\' Não')
        connec.updateStep(TABLE, id, 0.3)
    elif validate_registration:
        if text.upper().__eq__('S'):
            print('Correto!')
            print('Bem vindo {}'.format(connec.formatter(check.getName(id))))
            print('Você gostaria de responder um questionario? - \'S\' Sim e \'N\' Não')
            connec.updateStep(TABLE, id, 2.0)
        elif text.upper().__eq__('N'):
            print('Informe Seu Primeiro Nome?')
            connec.updateStep(TABLE, id, 0.2)
        else:
            print('Opcao invalida, tente novamente!')
            print(f'{connec.formatter(check.getName(id))}, Seu Nome esta correto? - \'S\' Sim e \'N\' Não')

    elif questions:
        checkQuestion(step, id, text)

    elif validate_questions:
        if text.upper().__eq__('S'):
            # Realizar primera pergunta
            print(list_questions.get('1'))
            connec.updateStep(TABLE, id, 1.1)
        elif text.upper().__eq__('N'):
            print('Obrigado pela oportunidade!')
            connec.updateStep(TABLE, id, 3.0)
        else:
            print('Opcao invalida, tente novamente!')
            print('Você gostaria de responder um questionario? - \'S\' Sim e \'N\' Não')

    elif challenges:
        print('Diga que voce é lindo!')
    else:
        print('NOT FOUND')


def checkBase(id):
    return check('').checkExist(id)


def checkQuestion(step, id, text):
    if check('').getStep(id).__eq__('1.1'):
        quest = "'" + text + "'"
        connec.updateQuestions(TABLE, id, quest)
        connec.updateStep(TABLE, id, '1.2')
        print(list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.2'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        print('\'S\' Sim, \'N\' Não ou \'T\' Talvez')
        print(list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.18'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        print(list_questions.get(str(int(check('').getStep(id)[2:]))))

    elif check('').getStep(id).__eq__('1.28'):
        connec.updateQuestions(TABLE, id, getQuest(id, text))
        connec.updateStep(TABLE, id, getNextQuestion(id))
        print('Obrigado Por responder o questionario')

    else:
        if text.upper().__eq__('S'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            print(list_questions.get(str(int(check('').getStep(id)[2:]))))
        elif text.upper().__eq__('N'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            print(list_questions.get(str(int(check('').getStep(id)[2:]))))
        elif text.upper().__eq__('T'):
            connec.updateQuestions(TABLE, id, getQuest(id, text))
            connec.updateStep(TABLE, id, getNextQuestion(id))
            print(list_questions.get(str(int(check('').getStep(id)[2:]))))
        else:
            print('Opcao invalida, tente novamente!')
            print('\'S\' Sim, \'N\' Não ou \'T\' Talvez')
            print(list_questions.get(str(int(check('').getStep(id)[2:]))))


def getNextQuestion(id):
    next = '1.' + str(float(check('').getStep(id)[2:]) + 1).replace('.0','')
    return "'"+next+"'"

def getQuest(id, text):
    return "'" + check('').getQuestions(id) + ';' + text + "'"


# id = '2243977022367260'

# if checkBase(id):
#     if check('').getStep(id).__eq__(step2):
#         print('Fazer Cadastro')
#         name = input()
#         startStep(step2, id, name)
#
#     elif check('').getStep(id).__eq__(step3):
#         print('Valida Nome')
#         choice = input()
#         startStep(step3, id, choice)
#
#     elif check('').getStep(id).__contains__('1.'):
#         if not check('').getStep(id).__eq__('1.29'):
#             print('perguntas')
#             choice = input()
#             startStep(step4, id, choice)
#         else:
#             print('challenges p')
#
#     elif check('').getStep(id).__eq__(step5):
#         print('Seq Pergunta')
#         choice = input()
#         startStep(step5, id, choice)
#     else:
#         # connec.updateStep(TABLE, id, 2.0)
#         if check('').getQuestions(id).__eq__(''):
#             choice = ''
#             if choice.upper().__eq__('S'):
#                 connec.updateStep(TABLE, id, 2.0)
#                 print('quer fazer o questionario')
#             elif choice.upper().__eq__('N'):
#                 print('quer fazer o questionario')
#             else:
#                 print('Opcao invalida, tente novamente!')
#                 print('\'S\' Sim ou \'N\' Não')
#             choice = input()
#
#
# else:
#     print('Primeira vez')
#     startStep(step1, id, '')

