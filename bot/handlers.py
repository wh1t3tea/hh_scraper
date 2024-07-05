import logging
import os
from datetime import datetime

import aiohttp
from aiogram import Dispatcher, types
from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message, \
    ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from filters import vacancy_filters
from parser import ParserOutHandler
from utils import form_answer, get_area_id, create_sheet

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

state_router = Router()
command_router = Router()
callback_router = Router()

API_ROUTE = os.environ["API_ROUTE"]
SCRAPER_ROUTE = os.environ["SCRAPER_ROUTE"]


class Form(StatesGroup):
    MainMenu = State()
    ParseVacancies = State()
    VacancyName = State()
    SalaryFrom = State()
    EmploymentType = State()
    Experience = State()
    SalaryOnly = State()
    CountVacancy = State()
    GetFromDB = State()
    SaveFilter = State()
    Start = State()


async def fetch_vacancy_data(session, user_data):
    async with session.get(url=SCRAPER_ROUTE, params=user_data) as response:
        return await response.json()


@state_router.message(Form.Start)
@command_router.message(Command('start'))
async def main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Here you can parse hh.ru or get saved data.\nUse /parse to start parsing.\nUse /analytics to get "
        "analytics\nUse /start to back to Main Menu")


@command_router.message(Command('analytics'))
async def get_analytics(message: types.Message, state: FSMContext):
    await state.clear()

    async with aiohttp.ClientSession() as session:
        async with session.get(os.environ["API_ANALYTICS_ROUTE"]) as response:
            stats = await response.json()

    stats_text = [f"Average salary: {round(stats['avg_salary_from'])}", f"Vacancy count: {stats['vacancy_count']}"]

    if len(stats["top_text_words"]) > 0:
        top_text_s = '\n'.join(
            [f"   - {stats['top_text_words'][i]['word']}: {stats['top_text_words'][i]['count']} times" for i in
             range(len(stats["top_text_words"]))])
        stats_text.append(f"Top key words:\n {top_text_s}")

    if len(stats["top_area_words"]) > 0:
        top_area_s = '\n'.join(
            [f"   - {stats['top_area_words'][i]['word']}: {stats['top_area_words'][i]['count']} times" for i in
             range(len(stats["top_area_words"]))])
        stats_text.append(f"Top areas:\n {top_area_s}")

    stats_text = "\n".join(stats_text)

    await message.answer(stats_text)
    await state.set_state(Form.Start)


@state_router.message(Form.MainMenu)
@command_router.message(Command('parse'))
async def parse(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    await state.set_state(Form.VacancyName)
    await message.answer("Send the vacancy name you want to search for:", reply_markup=ReplyKeyboardRemove())


@state_router.message(Form.VacancyName)
async def get_vacancy_name(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    await state.update_data(name=message.text)
    await state.set_state(Form.SalaryFrom)

    salary_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[[KeyboardButton(text='Skip')]])

    await message.answer("Send the average salary RUB (or type 'skip' to skip):", reply_markup=salary_kb)


@state_router.message(Form.SalaryFrom)
async def get_salary_from(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    salary = message.text

    if str(salary).isnumeric():
        if int(salary) > 0:
            await state.update_data(salary=salary)

    await state.set_state(Form.EmploymentType)

    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Full time'), KeyboardButton(text='Part time'))
    builder.add(KeyboardButton(text='Project'), KeyboardButton(text='Probation'))
    builder.adjust(2)

    await message.answer("Choose employment type:",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@state_router.message(Form.EmploymentType)
async def get_employment_type(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    employment_dict = {
        'Full time': 'full',
        'Part time': 'part',
        'Project': 'project',
        'Probation': 'probation'
    }

    data = employment_dict.get(message.text, None)

    if data is not None:
        await state.update_data(employment=data)

    await state.set_state(Form.Experience)

    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='No experience'), KeyboardButton(text='Between 1 and 3 years'))
    builder.add(KeyboardButton(text='Between 3 and 6 years'), KeyboardButton(text='More than 6 years'))
    builder.adjust(2)

    await message.answer("Choose experience level:",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@state_router.message(Form.Experience)
async def get_experience(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    experience_dict = {
        'No experience': 'noExperience',
        'Between 1 and 3 years': 'between1And3',
        'Between 3 and 6 years': 'between3And6',
        'More than 6 years': 'moreThan6'
    }

    data = experience_dict.get(message.text, None)

    if data is not None:
        await state.update_data(experience=data)

    await state.set_state(Form.SalaryOnly)

    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Yes'), KeyboardButton(text='No'))
    builder.adjust(1)

    await message.answer("Show vacancies with salary only? (Yes/No):",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@state_router.message(Form.SalaryOnly)
async def get_salary_only(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    await state.update_data(only_with_salary=int(message.text.lower() == 'yes'))
    await state.set_state(Form.CountVacancy)

    await message.answer("In which city do you want to look for vacancies?",
                         reply_markup=ReplyKeyboardRemove())


@state_router.message(Form.CountVacancy)
async def get_num_vacancies(message: Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    async with aiohttp.ClientSession() as session:
        url = 'https://api.hh.ru/areas/113'
        async with session.get(url) as response:
            areas_info = await response.json()

    city_id = get_area_id(message, areas_info)

    if city_id is not None:
        await state.update_data(area=city_id)

    await state.update_data(page=0)

    user_data = await state.get_data()

    async with aiohttp.ClientSession() as session:

        vacancy_data = await fetch_vacancy_data(session, user_data)
        pages = vacancy_data["pages"]

        for page in range(1, pages):
            user_data["page"] = page
            data = await fetch_vacancy_data(session, user_data)

            vacancy_data["items"] += data['items']

    data = ParserOutHandler(vacancy_data, n_vacancies=20)

    #try:
    await data.save_to_db()
    #except:
        #kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="back to menu")]], resize_keyboard=True)
        #await state.clear()
        #await state.set_state(Form.MainMenu)
        #await message.answer("Can't find any vacancies with selected filters",
        #                     reply_markup=kb)
        #return 0

    vac_to_show = await data.get_vacancies_to_show()
    message_parts = form_answer(vac_to_show)

    message_text = '\n\n'.join(message_parts)
    await message.answer(message_text, parse_mode=ParseMode.HTML)

    await state.clear()


@command_router.message(Command('get_from_db'))
async def get_vacancies_from_db(message: Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    kbs = [[InlineKeyboardButton(text=key, callback_data=value)] for key, value in vacancy_filters.items()]
    kbs.append([InlineKeyboardButton(text="Search with selected filters", callback_data="apply")])
    filter_buttons = InlineKeyboardMarkup(
        inline_keyboard=kbs
    )
    await message.answer("Select filters to search data from the database", reply_markup=filter_buttons)
    await state.set_state(Form.GetFromDB)


@state_router.message(Form.SaveFilter)
async def save_filter(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer("Main menu")
        await state.clear()
        await state.set_state(Form.Start)
        return 0

    logging.info("here")
    data = await state.get_data()
    filter_name = data.get("current_filter")
    if filter_name:
        await state.update_data({filter_name: message.text})
        await message.answer(f"Filter {filter_name} was successfully applied.")
    await state.set_state(Form.GetFromDB)


@callback_router.callback_query(lambda c: c.data in vacancy_filters.values())
async def filter_data(call: CallbackQuery, state: FSMContext):
    await call.answer()

    filter_key = call.data

    await state.update_data(current_filter=filter_key)

    await call.message.answer(f"Selected filter: {filter_key}")
    await state.set_state(Form.SaveFilter)


# TODO
@callback_router.callback_query(lambda call: call.data == "apply")
async def search_in_db(call: CallbackQuery, state: FSMContext):
    filters = await state.get_data()
    filters.pop("current_filter")

    async with aiohttp.ClientSession() as session:
        async with session.get(API_ROUTE, params=filters) as response:
            if response.status == 200:
                response_data = await response.json()

                if not isinstance(response_data, list):
                    response_data = [response_data]

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                await call.message.answer(f"Wait, we are writing your table...")

                sheet_url = await create_sheet(response_data, str(dt_string))

                await call.message.answer(f"Google Sheet table: {sheet_url}")
            else:
                await call.message.answer("Failed to find data with selected filters")

            await state.clear()
