import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from tools.raw_data_prepare.r2_metaData_extractor import WTF
from model_worker import predict_class_in_text, predict_class_in_photo
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, bold  # , italic, code, pre
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from settings import BOT_TOKEN, logger, TMP_FILE_LOCATION  # , MODEL_NAME


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

ELF_FILE_NAME = ""

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer('Hi! Give me the ELF file to analyse.\n\n Use the /help, '
                        'to known all command!')


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    message_text = text(bold('There is '), '`ELF_bot v0.0.1.`', bold(' What I can do today: \n'),
      '\t`/start` - in first send me a file in ELF format (usally, with .o extension)\n', 
      '\t`/funcs_list` - I return to you a list of funcs what I can found\n',
      '\t`/funcs_count` - I return to you a count of funcs what I can found\n',
      '\t`/what_the_func` - with a ML magic I try to predict a classes of all you func and return a pictire\n')
    await message.answer(message_text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=["funcs_count"])
async def process_help_command(message: types.Message):
        if not(os.path.exists(TMP_FILE_LOCATION)):
            await message.answer("In first you need to upload me ELF file. Use command /help for more information")
            return

        try: 
            wtf = WTF(path_to_binary_file="../." + TMP_FILE_LOCATION)
            founded_func_count = await wtf.get_functions_count()
            if founded_func_count == 0:
                await message.answer("Sorry, I'm not found functions in your file, try another file with /start")
            else:
                await message.answer("In you file I can fount {} functions. To predict classes send command /what_the_func".format(founded_func_count))

        except Exception as err:
            logger.error("Error while parsing file for func count", exc_info=err)
            await message.reply(f"Error while parsing file for func count:\n\n{err}")


@dp.message_handler(commands=["funcs_list"])
async def process_help_command(message: types.Message):
        if not (os.path.exists(TMP_FILE_LOCATION)):
            await message.answer("In first you need to upload me ELF file. Use command /help for more information")
            return

        try:
            wtf = WTF(path_to_binary_file= "../." + TMP_FILE_LOCATION)
            founded_funcs_list = await wtf.get_functions_names()
            if len(founded_funcs_list) == 0:
                await message.answer("Sorry, I'm not found functions in your file, try another file with /start")
            else:
                if len(founded_funcs_list) <= 20:
                    await message.answer("In you file I can fount `{}` functions: ".format(len(founded_funcs_list)),
                                          parse_mode=ParseMode.MARKDOWN)
                    text_list = ""
                    for func in founded_funcs_list:
                        text_list += "\t" + ("{}".format(func)) + "\n"                    
                else:
                    await message.answer("In you file I can fount `{}` functions. But I can show you only first `10` of them: ".format(len(founded_funcs_list)),
                                          parse_mode=ParseMode.MARKDOWN)
                    text_list = ""
                    list_10 = founded_funcs_list[slice(10)]
                    for func in list_10:
                        text_list += "\t" + ("{}".format(func)) + "\n"
                await message.answer(text_list)  # , parse_mode=ParseMode.MARKDOWN)


        except Exception as err:
            logger.error("Error while parsing file for func names", exc_info=err)
            await message.reply(f"Error while parsing file for func names:\n\n{err}")


@dp.message_handler(commands=["what_the_func"])
async def process_help_command(message: types.Message):
        if not(os.path.exists(TMP_FILE_LOCATION)):
            await message.answer("In first you need to upload me ELF file. Use command /help for more information")
            return

        try: 

            # TODO: check the headers of ELF
            await message.reply("Wait to file analyse...")
            logger.info("Start analyse...")


            wtf = WTF(path_to_binary_file= "../." + TMP_FILE_LOCATION)

            # get functions list with the raw asm cod
            raw_asm_dict = await wtf.get_functions_asm_code(get_the_graph=True)
            logger.info("Done getting raw asm code")


            list_of_code_and_cfg = list(raw_asm_dict.values())
            counter_of_predictions = await predict_class_in_text(list_of_code_and_cfg)
            logger.info("Done predict class")
            logger.info("Predicted: {}".format(counter_of_predictions.most_common(8))) 


            photo_of_predictions = await predict_class_in_photo(list_of_code_and_cfg, title_photo = ELF_FILE_NAME)            
            await bot.send_photo(message.from_user.id, photo_of_predictions,
                         caption= "Predictions for all funcs in your ELF file", 
                         reply_to_message_id=message.message_id)

            logger.info("All jobs is done!!!!") 

        except Exception as err:
            logger.error("Error while parsing file", exc_info=err)
            await message.reply(f"Error while parsing file:\n\n{err}")


@dp.message_handler()
async def get_summary(message: types.Message):
    try:

        type_ct = message.content_type
        logger.info("Content type: {}".format(type_ct))
        if type_ct == "text":
            user_input = message.text.strip()
        else:
            return

        if not user_input.startswith("ELF"): 
            await message.reply(
                "Please start text from ELF word"
            )
            return

        await message.reply("OK! But I'm not a chart-bot. See /help") 

    except Exception as err:
        logger.error("Error while parsing file", exc_info=err)
        await message.reply(f"Error while parsing file:\n\n{err}")


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    type_ct = msg.content_type
    logger.info("Content type: {}".format(type_ct))
    if type_ct == "photo":
        await msg.reply("Thanks, fanny photo! but I need ELF file")
        return
    
    if type_ct == "document":
        global ELF_FILE_NAME
        ELF_FILE_NAME = msg.document.file_name
        logger.info("Load file: {}".format(msg.document.file_name))
        file_id = msg.document.file_id

        file = await bot.get_file(file_id)
        file_path = file.file_path
        my_object = await bot.download_file(file_path = file_path)  # Getting the File represented as a BytesIO Object
        
        logger.info("Saved tmp file to : {}".format(TMP_FILE_LOCATION))
        with open(TMP_FILE_LOCATION, 'wb') as out:  # Open temporary file as bytes
            out.write(my_object.read())                # Read bytes into file


if __name__ == "__main__":
    if (os.path.exists(TMP_FILE_LOCATION)): # remove last file. TODO: store in DB
        os.remove(TMP_FILE_LOCATION)
    executor.start_polling(dp, skip_updates=True)