import discord
from discord.ext import commands
import random
import requests
import requests
from translate import Translator

with open('DS_TOKEN', 'r') as file:
    DS_TOKEN = file.read().strip()


def get_trivia_questions():
    url = "https://opentdb.com/api.php?amount=5&type=multiple"
    response = requests.get(url)
    data = response.json()
    return data["results"]


def translate_text(text, target_language="es"):
    translator = Translator(to_lang=target_language)
    return translator.translate(text)


def get_translated_trivia():
    questions = get_trivia_questions()
    translated_questions = []

    for q in questions:
        question = translate_text(q["question"])
        correct_answer = translate_text(q["correct_answer"])
        incorrect_answers = [translate_text(ans) for ans in q["incorrect_answers"]]

        translated_questions.append({
            "question": question,
            "correct_answer": correct_answer,
            "incorrect_answers": incorrect_answers
        })

    return translated_questions


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

active_questions = {}  

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


@bot.tree.command(name="trivia")
async def trivia(interaction: discord.Interaction):
    await interaction.response.defer()  

    questions = get_translated_trivia()
    question = questions[0]  

    
    options = question["incorrect_answers"] + [question["correct_answer"]]
    random.shuffle(options)


    await interaction.followup.send(
        f"**Pregunta:** {question['question']}\n\n" +
        "\n".join([f"{i+1}. {option}" for i, option in enumerate(options)])
    )


@bot.event
async def on_message(message):
    # Ignorar mensajes del bot
    if message.author == bot.user:
        return

    
    question_data = active_questions.get(message.channel.id)
    if question_data:
        try:
            
            selected_option = int(message.content.strip()) - 1
            if 0 <= selected_option < len(question_data["options"]):  # Verificar opción válida
                selected_answer = question_data["options"][selected_option]

                
                if selected_answer == question_data["correct_answer"]:
                    await message.channel.send(f"🎉 ¡Correcto! La respuesta era: **{selected_answer}**")
                else:
                    await message.channel.send(f"❌ Incorrecto. La respuesta correcta era: **{question_data['correct_answer']}**")

                
                del active_questions[message.channel.id]
            else:
                await message.channel.send("Por favor, selecciona un número válido entre las opciones.")
        except ValueError:
            await message.channel.send("Por favor, escribe un número válido (1, 2, 3 o 4).")
    else:
      
        await bot.process_commands(message)




bot.run(DS_TOKEN)
