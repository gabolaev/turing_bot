import glob

from sympy import *
from telebot import types

import bot
import config
import dbUtils

toCreate = {'problem': 3, 'solution': 4, 'answer': 5}


### ЕГЭ

def latex2image(recordOfProblem):
    try:
        for i in toCreate:
            if recordOfProblem[toCreate[i]]:
                pathFormat = [(2 if recordOfProblem[10] >= 13 else 1), recordOfProblem[10], i, recordOfProblem[10][1], i]
                preview(r'{}'.format(recordOfProblem[10][toCreate[i]]),
                        viewer='file',
                        output='png',
                        preamble=config.myPreamble,
                        filename=config.bankPath + config.egeTaskPathPattern.format(*pathFormat),
                        dvioptions=config.dviOptions
                        )
    except Exception:
        bot.logging(text=config.latex2pngError)


def checkImageExist(recordOfProblem):
    try:
        pathFormat = [(2 if recordOfProblem[10] >= 13 else 1), recordOfProblem[10], 'problem', recordOfProblem[1], 'problem']
        open(config.bankPath + config.egeTaskPathPattern.format(*pathFormat, 'r')).close()
    except IOError:
        latex2image(recordOfProblem)


def getEgeProblem(recordOfProblem):

    checkImageExist(recordOfProblem)

    problemKeyboard = types.InlineKeyboardMarkup(row_width=2)
    constrProblemKeyboard = []

    path = config.bankPath + config.egeTaskPathPattern.format((2 if recordOfProblem[10] >= 13 else 1), recordOfProblem[10], 'problem',
                                                              recordOfProblem[1], 'problem')

    solutndsolv = ['answer', 'solution']
    for i in solutndsolv:
        try:
            tryPath = path.replace('problem', i).replace('problem', i)
            open(tryPath, 'r').close()
            constrProblemKeyboard.append(dict(text='Решение' if i == 'solution' else 'Ответ', callback_data=tryPath))
        except IOError:
            pass

    problemKeyboard.keyboard = [constrProblemKeyboard]
    return recordOfProblem[0], path, problemKeyboard, tags


### ЕГЭ

### ДВИ

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


### ДВИ

### Ларин

def getFileWithoutExtension(path):
    from os.path import basename, splitext
    return splitext(basename(path))[0]


def chunks(listOfVariants, sizes):
    for i in range(0, len(listOfVariants), sizes):
        yield listOfVariants[i:i + sizes]


def getLarinVariantsKeyboard():
    variantsKeyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True).row('🔙В начало')

    variantsNumbers = sorted(
        [int(getFileWithoutExtension(a)) for a in glob.glob(config.bankPath + config.larinPathPattern)], reverse=True)

    partedVariants = list(chunks(variantsNumbers, 4))

    for foury in partedVariants:
        variantsKeyboard.keyboard.append([dict(text='Вар. {}'.format(i)) for i in foury])

    return variantsKeyboard

    ###Ларин
