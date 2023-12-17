from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.types import ContentType
import config  # здесь находится токен нашего бота
from labs import dict_for_dnkom, dict_for_Unilab, dict_for_KDL
import json
main_dict = 0

# Global variable to store the main dictionary of symptoms and tests.

bot = Bot(config.TOKEN_API)
dp = Dispatcher(bot)
# This function creates a new Bot instance using the token provided in the config
# module,and then creates a Dispatcher for this bot, which helps in managing the incoming updates.
# The remaining code for command handlers and other functions goes here.
# Dictionaries to store mappings of symptoms to recommended medical tests.
# Each dictionary is tailored to a specific medical laboratory's test offerings.

spsiok_dlya_krovi = 'Секуться волосы, Деформация ногтей, Заеды в углах рта , Изчерченность ногтей , Слабость'
# Symptom combination for which you must donate blood
spsiok_dlya_ureznu_test = 'Боль в области желудка'
# Symptom combination for which you must do ureznu test
spsiok_dlya_kal = 'Боль в области желудка'

# Состояние выбранных номеров
selected_symptoms = set()
name_of_lab = ''


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):  # тут мы обрабатываем команду start и выдаем начальный текст
    """
    Handles the /start command sent by the user. Displays a welcome message and offers a choice of laboratories for
    medical tests.

    Args:
        message (types.Message): The message from the user containing the /start command.

    Returns:
        None: This function sends messages back to the user via the bot's asynchronous interface but does not return
        any value.

    """
    selected_symptoms.clear()
    ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='ДНКОМ⠀')
    b2 = KeyboardButton(text='KDL⠀')
    b3 = KeyboardButton(text='Юнилаб⠀')
    ikb.add(b1, b2, b3)
    welcome_text = (
        f'Друзья, данный ресурс поможет понять какое обследование нужно пройти именно Вам, чтобы оценить '
        f'прицельно Ваше здоровье, выявить какие-либо патологии, понять причины симптомов / недугов\n'
        'Пожалуйста, выберите лабораторию, в которой Вы планируете обследоваться'
    )
    await message.answer(text=welcome_text, reply_markup=ikb)


def changing_lab(text):
    """
        The changing_lab function serves to enable switching lab-related variables, specifically main_dict
        and name_of_lab, based on the provided text

        Args:
        text (string): The text specifying the designated laboratory or the request to switch to another one.

        Returns:
            Tuple: The tuple contains two elements representing the chosen laboratory's name and its
            associated dictionary or data structure. Element 1: name_of_lab (string) - The name of
            the selected laboratory. Element 2: main_dict (type determined by the laboratory)
             - A data structure representing the selected laboratory

        Examples : Switching to the "DNKOM" laboratory name, lab_dict = changing_lab('Switch to DNKOM')

    """
    global main_dict
    global name_of_lab
    if text == 'ДНКОМ⠀' or text == 'Поменять на ДНКОМ⠀':
        name_of_lab = 'ДНКОМ'
        main_dict = dict_for_dnkom
        return name_of_lab, main_dict
    elif text == 'KDL⠀' or text == 'Поменять на KDL⠀':
        name_of_lab = 'KDL'
        main_dict = dict_for_KDL
        return name_of_lab, main_dict
    elif text == 'Юнилаб⠀' or text == 'Поменять на Юнилаб⠀':
        name_of_lab = 'Юнилаб'
        main_dict = dict_for_Unilab
        return name_of_lab, main_dict
    else:
        return 0


@dp.message_handler(text=['ДНКОМ⠀', 'KDL⠀', 'Юнилаб⠀', 'Корректировка⠀'])  # обращаемся к диспетчеру
async def chosing_symptoms(message: types.Message):  # тут обрабатываем текст 'ДНКОМ', 'KDL', 'Юнилаб' и исходя
    # из выбранной лаборатории меняем main_dict на лабораторию, далее предлагем кнопки по
    # которым человек выбирает симптомы, если был подан текст 'Корректировка', то мы
    # обнуляем список выбранных ранее симпотов и поторяем выбор кнопками
    """
    Presents a list of symptoms for the user to choose from, depending on the selected laboratory or clear
    selected_symptoms and continue process. The function sets up an inline keyboard with symptoms and a button to finish
    the selection. This function use callback to do a list of selected symptoms.

    Args:
    message (types.Message): The message from the user selecting the laboratory.

    Returns:
        None: Sends a message to the user with a list of symptoms to choose from and does not return any value.

    """
    changing_lab(message.text)
    selected_symptoms.clear()
    keyboard_markup = types.InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text='Секуться волосы', callback_data='number_Секуться волосы')
    b2 = InlineKeyboardButton(text='Деформация ногтей', callback_data='number_Деформация ногтей')
    b3 = InlineKeyboardButton(text='Заеды в углах рта', callback_data='number_Заеды в углах рта')
    b4 = InlineKeyboardButton(text='Изчерченность ногтей', callback_data='number_Изчерченность ногтей')
    b5 = InlineKeyboardButton(text='Боль в области желудка', callback_data='number_Боль в области желудка')
    b6 = InlineKeyboardButton(text='Слабость', callback_data='number_Слабость')
    b7 = InlineKeyboardButton(text='Закончить выбор', callback_data='number_Закончить выбор')
    keyboard_markup.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6).add(b7)
    await message.answer(
        "Выберите один или несколько симптомов(при повторном нажатии на симпотом, он исчезает)."
        " Для того, чтобы закончить выбор, нажмите на 'Закончить выбор'",
        reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('number_'))
async def process_callback_checkbox(callback_query: types.CallbackQuery):  # тут обработчик callBack, который
    # обрабатывает выбранные симптомы и собирает их в список
    """
    Processes the callback from the inline buttons used for symptom selection. Adds or removes symptoms from the
    selection set based on user interaction. Sends a completion message once the user finishes selecting symptoms.

    Args:
        callback_query (types.CallbackQuery): The callback query from the inline buttons, containing the
        selected symptom.

    Returns:
         None: Responds to the callback query and updates the user's symptom selection but does not return any values.

    """
    # For example:User select ‘Секуться волосы’ and ‘Слабость’.And this function make a list
    # with these symptoms and output the result

    symptom = callback_query.data.split("_")[1]
    if symptom in selected_symptoms:
        selected_symptoms.remove(symptom)
    else:
        if symptom == 'Закончить выбор':
            if len(selected_symptoms) > 0:
                selected_symptoms_message = ", ".join(str(num) for num in selected_symptoms)
                ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                b1 = KeyboardButton(text='Далее⠀')
                b2 = KeyboardButton(text='Корректировка⠀')
                ikb.add(b1, b2)
                await bot.send_message(callback_query.message.chat.id, text=f'Вы выбрали такие '
                                                                            f'варианты: {selected_symptoms_message}.')
                await bot.send_message(callback_query.message.chat.id,
                                       text='Если перечень симптомов верен - нажмите "Далее"'
                                            '. \nЕсли требуются исправления '
                                            '- нажмите "Корректировка"',
                                       reply_markup=ikb)
                await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            else:
                await bot.answer_callback_query(callback_query.id, text=f"Вы не выбрали симптомы")

        else:
            selected_symptoms.add(symptom)
    selected_symptoms_message = ", ".join(str(num) for num in selected_symptoms)
    await bot.answer_callback_query(callback_query.id, text=f"Вы выбрали: {selected_symptoms_message}")


@dp.message_handler(text=['Далее⠀'])  # обращаемся к диспетчеру
async def process_dalee_command(message: types.Message):  # тут мы обрабатываем текст 'Далее' и после этого
    # основываясь на main_dict выдаем нужную информацию об лаборатории
    """
    Processes the 'Далее' command from the user. Based on the selected laboratory (main_dict), it provides specific
    information about the laboratory and the next steps in the process.

    Args:
        message (types.Message): The message from the user indicating they wish to proceed with the selected
        laboratory's procedures.

    Returns:
        None: Sends messages regarding the laboratory details and next steps but does not return any values.

    """

    ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='Получить анализы⠀')
    b2 = KeyboardButton(text='Поменять лабораторию⠀')
    ikb.add(b1, b2)
    await message.answer(
        text=f'Так как вы выбрали {name_of_lab} для обследование, то, пожалуйста,'
             f' обратите ВНИМАНИЕ на следующие сообщения')
    if name_of_lab == 'ДНКОМ':
        with open('skidka_dnkomm.json', 'r', encoding='utf-8') as file:
            promo_data = json.load(file)
        await message.answer(
            text=promo_data["promo_information"])
    elif name_of_lab == 'KDL':
        with open('skidka_kdll.json', 'r', encoding='utf-8') as file:
            promo_data = json.load(file)
        await message.answer(
            text=promo_data["text1"])
        await message.answer(
            text=promo_data["text2"])
        photo = open('skidka.png', 'rb')
        await bot.send_photo(message.chat.id, photo)
    await message.answer(
        text=f'Результаты от {name_of_lab} Вы можете БЕСПЛАТНО отправлять мне на интерпретацию '
             f'и назначения через ресурсы сайта! \n*в течение месяца \nhttps://ershovlabexpert.ru/intrepretation')
    await message.answer(
        text=f'Если вы хотите получить список анализов, которые вам нужно сдать, нажмите "Получить'
             f' анализы"\nЕсли хотите поменять лабораторию, нажмите "Поменять лабораторию"',
        reply_markup=ikb)


@dp.message_handler(text=['Поменять лабораторию⠀', 'Поменять еще раз лабораторию⠀'])  # обращаемся к диспетчеру
async def process_change_command(message: types.Message):  # получаем информацию на какую именно поменять лабораторию
    """
    Handles the ‘Поменять лабораторию’ command or the ‘Поменять еще раз лабораторию’ command sent by the user.
    Displays offers a choice of laboratories for medical tests that user wants to change.

    Args:
        message (types.Message): The message from the user selecting the laboratory that wants to change.

    Returns:
        None: Send message with the new laboratory that they want to change but does not return any values
    """
    ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='Поменять на ДНКОМ⠀')
    b2 = KeyboardButton(text='Поменять на KDL⠀')
    b3 = KeyboardButton(text='Поменять на Юнилаб⠀')
    ikb.add(b1, b2, b3)
    await message.answer(text='Пожалуйста, выберите другую лабораторию, в которой Вы планируете обследоваться',
                         reply_markup=ikb)


@dp.message_handler(text=['Поменять на KDL⠀', 'Поменять на ДНКОМ⠀', 'Поменять на Юнилаб⠀'])  # обращаемся к диспетчеру
async def process_change_to_new_lab_command(message: types.Message):  # Тут мы обрабатываем текст
    # 'Поменять на KDL', 'Поменять на ДНКОМ', 'Поменять на Юнилаб' и меняем main_dict на новую лабораторию
    """
    This function change the mian_dict to new laboratory, that user chose. Displays offers a choice of two buttons:
     ‘Поменять еще раз лабораторию’(this text calls previous function) ‘Далее’(This text calls function
     process_dalee_command).

    Args:
        message (types.Message): The message from the user on which.

    Returns:
        None: Send message with the new laboratory that they want to change but does not return any values

    """
    changing_lab(message.text)
    ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='Далее⠀')
    b2 = KeyboardButton(text='Поменять еще раз лабораторию⠀')
    ikb.add(b1, b2)
    await message.answer(
        text=f'Ваша новая лаборатория - {name_of_lab}.\nЕсли лаборатория выбрана верно, нажмите кнопку "Далее"\nЕсли '
             f'хотите снова помянять лабораторию, нажмите кнопку "Поменять еще раз лабораторию"',
        reply_markup=ikb)


@dp.message_handler(text=['Получить анализы⠀'])
async def process_get_analizy_command(message: types.Message):  # тут мы обрабатывае текст
    # "Получить анализы" и далее выдаем их
    """
    Maps a set of symptoms to recommended medical tests.This function uses predefined dictionaries for different
    medical laboratories to map the collected symptoms to a set of recommended tests. And recommendation for tests

    Args:
        message (types.Message):  A tuple of symptoms provided by the user.

    Returns:
         None: Send message with a string containing the recommended medical tests. And recommendation for tests

    """
    global selected_symptoms
    sovet = set()
    selected_symptoms_message2 = set()
    for j in selected_symptoms:
        for i in main_dict.keys():
            if j in i:
                if j in spsiok_dlya_krovi:
                    sovet.add('КРОВЬ (венозная). Сдавать утром натощак, ничего с вечера жирного не есть.')
                if j in spsiok_dlya_kal:
                    sovet.add('КАЛ утренний (при невозможности - с вечера с холодильника)')
                if j in spsiok_dlya_ureznu_test:
                    sovet.add('Уреазный (дыхательный) тест')
                selected_symptoms_message2.add(main_dict[i])
    final_answer = ''
    for b in selected_symptoms_message2:
        final_answer += b
    await message.answer(final_answer)
    message_sovet = ''
    for a in sovet:
        message_sovet += a+'\n'
    await message.answer(text=f'Обращаю Ваше внимание, что согласно списку исследований, сформированному'
                              f' на основании Ваших жалоб, в лаборатории необходимо будет '
                              f'сдать следующий материал:\n{message_sovet}')
    await message.answer(text='Чтобы перезапустить бота нужно написать / и выбрать'
                              ' из предложенных выше выриантов "/start"')


@dp.message_handler()
async def random_text(message: types.Message):  # обработка случайного текста, который ввел пользователь
    """
    Echoes the message sent by the user.This function acts as a fallback for unhandled messages. It simply echoes
    back whatever the user sends.

    Args:
        message (types.Message): The incoming message object from the user.

    Returns:
        None: This function sends a reply to the user echoing the received message.

    """
    await message.answer(
        text=f'Данный бот не расчитан на веденние текста. Для получения корректного ответа, выбирайте'
             f' из предложенных вариантов.\nЧтобы продолжить общение с ботом нажмите'
             f' на кнопку(с четырьмя точками) справа, где расположено поле для ввода сообщений')
    await message.answer(text='Кнопка выглядит вот так:')
    photo = open('knopka.png', 'rb')
    await bot.send_photo(message.chat.id, photo)


@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    """
    Echoes the photo sent by the user.This function acts as a fallback for unhandled photos.
    It simply echoes back whatever the user sends.

    Args:
        message (types.Message): The incoming photo object from the user.

    Returns:
        None: This function sends a reply to the user echoing the received message.

    """
    await message.answer(text=f'Прошу не отсылайте в этот бот фотографии.\nЧтобы продолжить общение с ботом нажмите'
                              f' на кнопку(с четырьмя точками) справа, где расположено поле для ввода сообщений')
    await message.answer(text='Кнопка выглядит вот так:')
    photo = open('knopka.png', 'rb')
    await bot.send_photo(message.chat.id, photo)


if __name__ == '__main__':
    executor.start_polling(dp)  # старт бота
# чтобы запустить бота, надо в терминале нуписать python и название файла с кодом от бота
# чтобы закончить работу бота надо нажать в терминале ctrl +c
