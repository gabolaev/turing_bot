import glob

from sympy import *
from telebot import types

import bot
import config
import dbUtils

toCreate = {'problem': 3, 'solution': 4, 'answer': 5}


def latex2image(record, egeNumber):
    try:
        for i in toCreate:
            if record[toCreate[i]]:
                preview(r'{}'.format(record[toCreate[i]]),
                        viewer='file',
                        output='png',
                        preamble=config.myPreamble,
                        filename=config.bankPath + config.egeTaskPathPattern.format((2 if egeNumber >= 13 else 1),
                                                                                    egeNumber,
                                                                                    i,
                                                                                    record[1],
                                                                                    i),
                        dvioptions=config.dviOptions
                        )
    except Exception:
        bot.logging(text=config.latex2pngError)


def checkImageExistAndGet(egeNumber):
    record, tagsWithoutNumber = dbUtils.getRandomProblemByEgeNumber(egeNumber)

    tags = 'Задача №{} ({})\n{}'.format(egeNumber, record[1], tagsWithoutNumber)
    try:
        open(config.bankPath + config.egeTaskPathPattern.format((2 if egeNumber >= 13 else 1),
                                                                egeNumber,
                                                                'problem',
                                                                record[1],
                                                                'problem'), 'r').close()
    except IOError:
        latex2image(record, egeNumber)
    return record, tags


def getDviProblem(year, variant):
    path = config.bankPath + config.dviProblemPathPattern.format(year, year, variant, 'problem')
    problemKeyboard = types.InlineKeyboardMarkup(row_width=1)
    try:
        solutionPath = path.replace('problem.png', 'solution.pdf')
        open(solutionPath).close()
        problemKeyboard.add(types.InlineKeyboardButton(text='Решение', callback_data=solutionPath))
    except Exception:
        pass

    tags = '#ДВИ' + str(year)
    return path, problemKeyboard, tags


def getFileWithoutExtension(path):
    from os.path import basename, splitext
    return (splitext(basename(path))[0])


def chunks(listOfVariants, sizes):
    for i in range(0, len(listOfVariants), sizes):
        yield listOfVariants[i:i + sizes]


def getLarinVariantsKeyboard():
    variantsKeyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True).row("🔙В начало")

    variantsNumbers = sorted(
        [int(getFileWithoutExtension(a)) for a in glob.glob(config.bankPath + config.larinPathPattern)], reverse=True)

    partedVariants = list(chunks(variantsNumbers, 4))

    for foury in partedVariants:
        fourLine = []
        for i in foury:
            fourLine.append(dict(text='Вар. {}'.format(i)))
        variantsKeyboard.keyboard.append(fourLine)

    return variantsKeyboard


def getEgeProblem(egeNumber):
    randomProblem, tags = checkImageExistAndGet(egeNumber)

    problemKeyboard = types.InlineKeyboardMarkup(row_width=2)
    constrProblemKeyboard = []

    path = config.bankPath + config.egeTaskPathPattern.format((2 if egeNumber >= 13 else 1), egeNumber, 'problem',
                                                              randomProblem[1], 'problem')

    solutndsolv = ['answer', 'solution']
    for i in solutndsolv:
        try:
            tryPath = path.replace('problem', i).replace('problem', i)
            open(tryPath, 'r').close()
            constrProblemKeyboard.append(dict(text='Решение' if i == 'solution' else "Ответ",
                                              callback_data=tryPath))
        except IOError:
            pass

    problemKeyboard.keyboard = [constrProblemKeyboard]
    return randomProblem[0], path, problemKeyboard, tags
