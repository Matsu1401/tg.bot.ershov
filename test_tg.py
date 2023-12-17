import pytest
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgggg import process_change_command
from tgggg import dict_for_dnkom
from tgggg import process_start_command
from tgggg import changing_lab


@pytest.mark.asyncio
async def test_process_change_command(mocker):
    message_mock = mocker.AsyncMock()  # Создаем экземпляр AsyncMock
    message_mock.answer = mocker.AsyncMock()  # Заменяем асинхронную функцию библиотеки на AsyncMock
    await process_change_command(message_mock)  # Вызываем асинхронную функцию и передаем в нее экземпляр AsyncMock
    expected_text = 'Пожалуйста, выберите другую лабораторию, в которой Вы планируете обследоваться'
    ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='Поменять на ДНКОМ⠀')
    b2 = KeyboardButton(text='Поменять на KDL⠀')
    b3 = KeyboardButton(text='Поменять на Юнилаб⠀')
    ikb.add(b1, b2, b3)
    expected_markup = ikb
    message_mock.answer.assert_awaited_once_with(
         text=expected_text,
         reply_markup=expected_markup
    )


@pytest.mark.asyncio
async def test_process_start_command(mocker):
    message_mock = mocker.AsyncMock()
    message_mock.answer = mocker.AsyncMock()
    await process_start_command(message_mock)
    expected_text = (f'Друзья, данный ресурс поможет понять какое обследование нужно пройти именно Вам, чтобы оценить '
                     f'прицельно Ваше здоровье, выявить какие-либо патологии, понять причины симптомов / недугов\n'
                     f'Пожалуйста, выберите лабораторию, в которой Вы планируете обследоваться')
    ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='ДНКОМ⠀')
    b2 = KeyboardButton(text='KDL⠀')
    b3 = KeyboardButton(text='Юнилаб⠀')
    ikb.add(b1, b2, b3)
    expected_reply_markup = ikb
    message_mock.answer.assert_awaited_once_with(text=expected_text, reply_markup=expected_reply_markup)


def test_changing_lab():
    # Исходные данные
    input_text = 'ДНКОМ⠀'
    # Вызов функции
    name_of_lab, main_dict = changing_lab(input_text)
    # Проверка ожидаемых результатов
    assert name_of_lab == 'ДНКОМ'
    assert main_dict == dict_for_dnkom


def test_unchanging_lab():
    # Исходные данные
    input_text = 'etbeatbae'
    # Вызов функции
    result = changing_lab(input_text)
    # Проверка ожидаемых результатов
    assert result == 0
