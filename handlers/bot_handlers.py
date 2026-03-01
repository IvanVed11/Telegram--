from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from keyboards.kb import Keyboard
from aiogram.fsm.context import FSMContext
from collections import defaultdict
from random import randint


from math_examples.creating_examples import MultiplicationTable
from states_floder.states import MultiplyState
from database.db import DatabaseBot

user_router = Router()
table = MultiplicationTable()
user_db = DatabaseBot()
kb_class = Keyboard()
mul_table = defaultdict(int, {"1":[[1,1,1],[1,2,2],[1,3,3],[1,4,4],[1,5,5],[1,6,6],[1,7,7],[1,8,8],[1,9,9]],"2":[[2,1,2],[2,2,4],[2,3,6],[2,4,8],[2,5,10],[2,6,12],[2,7,14],[2,8,16],[2,9,18]],"3":[[3,1,3],[3,2,6],[3,3,9],[3,4,12],[3,5,15],[3,6,18],[3,7,21],[3,8,24],[3,9,27]],"4":[[4,1,4],[4,2,8],[4,3,12],[4,4,16],[4,5,20],[4,6,24],[4,7,28],[4,8,32],[4,9,36]],"5":[[5,1,5],[5,2,10],[5,3,15],[5,4,20],[5,5,25],[5,6,30],[5,7,35],[5,8,40],[5,9,45]],"6":[[6,1,6],[6,2,12],[6,3,18],[6,4,24],[6,5,30],[6,6,36],[6,7,42],[6,8,48],[6,9,54]],"7":[[7,1,7],[7,2,14],[7,3,21],[7,4,28],[7,5,35],[7,6,42],[7,7,49],[7,8,56],[7,9,63]],"8":[[8,1,8],[8,2,16],[8,3,24],[8,4,32],[8,5,40],[8,6,48],[8,7,56],[8,8,64],[8,9,72]],"9":[[9,1,9],[9,2,18],[9,3,27],[9,4,36],[9,5,45],[9,6,54],[9,7,63],[9,8,72],[9,9,81]]})


@user_router.message(CommandStart())
async def start_bot(message: Message):
    keyboard = kb_class.multiplicate()
    await user_db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(text="Привет! 🎓 С моей помощью ты выучишь таблицу умножения быстро и легко. Давай тренироваться.", reply_markup=keyboard)


@user_router.message(Command(commands="help"))
async def help(message: Message):
    await message.answer('''Чтобы попасть в главное меню, введите команду /start .\n
Далее Вам нужно выбрать умножение на нужное число, нажав на соответствующую кнопку.\n
После этого бот выведет Вам пример. Для ввода ответа нажмите на подходящую кнопку.\n
Для вывода справки наберите команду /help .
                        ''')


@user_router.callback_query(F.data.startswith("x"))
async def mul_on_certain_num(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    factor = int(callback.data[1])
    num1, num2, ans = mul_table[str(factor)][randint(0, 8)]
    keyboard_with_answers = kb_class.generate_multiplicate_answers(ans)

    await state.set_state(MultiplyState.waiting_answer)
    await state.update_data(user_id = callback.from_user.id, right_answer=ans)

    await callback.message.answer(text=f"{num1} * {num2} = ?", reply_markup=keyboard_with_answers)



@user_router.message(MultiplyState.waiting_answer)
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    right_answer = str(data["right_answer"])
    is_right_ans = False

    if not message.text.isdigit():
        await message.reply("Выберите ответ в виде цифры.")

    elif message.text == right_answer:
        await message.reply("✅ Правильно!", reply_markup=ReplyKeyboardRemove())
        is_right_ans = True
        await user_db.update_stats(message.from_user.id, is_right_ans)
        await state.clear()
    else:
        await message.reply(f"❌ Неверно. Правильный ответ: <b>{right_answer}</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        await user_db.update_stats(message.from_user.id, is_right_ans)
        await state.clear()


@user_router.message(Command(commands="top"))
async def get_top_users(message: Message):
    top_users = await user_db.get_user_stats()
    text = "🏆 Топ 5 игроков:\n\n"
    for i, (first_name, score) in enumerate(top_users, start=1):
        name = first_name
        text += f"{i}. {name} — {score}\n"

    await message.answer(text)

@user_router.message(Command(commands="profile"))
async def view_profile(message: Message):
    profile = await user_db.get_profile_statistics(message.from_user.id)
    for row in profile:
        amount_solved_examples, amount_correctly_solved_examples, first_name = row
    text = f"📊Ваш профиль:\n\n"
    text += f"Решено примеров: {amount_solved_examples}\n"
    text += f"Правильных решений: {amount_correctly_solved_examples}\n"
    if amount_correctly_solved_examples != 0:
        text += f"Процент верных решений: {round(amount_correctly_solved_examples / amount_solved_examples * 100)}%"
    else:
         text += f"Процент верных решений: {0}%"
    await message.answer(text=text)

    
@user_router.message()
async def reply_on_text_msg(message: Message):
    await message.answer("Работа с ботом осуществляется только с помощью кнопок и команд /start , /help .")