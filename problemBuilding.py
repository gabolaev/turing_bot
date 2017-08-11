import glob
from sympy import *
from telebot import types
import bot
from config import *



### ЕГЭ {


def latex2image(recordOfProblem):
    toCreate = {'problem': 3, 'solution': 4, 'answer': 5}
    try:
        for i in toCreate:
            if recordOfProblem[toCreate[i]]:
                pathFormat = [(2 if recordOfProblem[7] >= 13 else 1), recordOfProblem[7], i, recordOfProblem[1],i]
                preview(r'{}'.format(recordOfProblem[toCreate[i]]),
                        viewer='file',
                        output='png',
                        preamble=myPreamble,
                        filename=bankPath + egeTaskPathPattern.format(*pathFormat),
                        dvioptions=dviOptions
                        )
    except Exception:
        bot.logging(text=latex2pngError)


def checkImageExist(recordOfProblem):
    try:
        pathFormat = [(2 if recordOfProblem[7] >= 13 else 1), recordOfProblem[7], 'problem', recordOfProblem[1], 'problem']
        open(bankPath + egeTaskPathPattern.format(*pathFormat, 'r')).close()
    except IOError:
        latex2image(recordOfProblem)


def getEgeProblem(recordOfProblem):

    checkImageExist(recordOfProblem[0])

    path = bankPath + egeTaskPathPattern.format((2 if recordOfProblem[0][7] >= 13 else 1),
                                                              recordOfProblem[0][7], 'problem',
                                                              recordOfProblem[0][1], 'problem')

    problemKeyboard = types.InlineKeyboardMarkup(row_width=2)
    constrProblemKeyboard = []
    for i in ['answer', 'solution']:
        try:
            tryPath = path.replace('problem', i).replace('problem', i)
            open(tryPath, 'r').close()
            constrProblemKeyboard.append(dict(text='Решение' if i == 'solution' else 'Ответ', callback_data=tryPath))
        except IOError:
            pass
    problemKeyboard.keyboard = [constrProblemKeyboard]

    tags = 'Задача №{} ({})\n{}'.format(recordOfProblem[0][7], recordOfProblem[0][1], recordOfProblem[1])
    return recordOfProblem[0][0], path, problemKeyboard, tags


### ЕГЭ }

### ДВИ {

def getDviProblem(year):
    path = bankPath + dviProblemPathPattern.format(year, year, 'problem')
    problemKeyboard = types.InlineKeyboardMarkup(row_width=1)

    solutionPath = path.replace('problem.pdf', 'solution.pdf')
    open(solutionPath).close()
    problemKeyboard.add(types.InlineKeyboardButton(text='Решение', callback_data=solutionPath))

    tags = '#ДВИ' + str(year)
    return path, problemKeyboard, tags


### ДВИ }

### Ларин {

def getFileWithoutExtension(path):
    from os.path import basename, splitext
    return splitext(basename(path))[0]


def chunks(listOfVariants, sizes):
    for i in range(0, len(listOfVariants), sizes):
        yield listOfVariants[i:i + sizes]


def getLarinVariantsKeyboard():
    variantsKeyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True).row('🔙В начало')

    variantsNumbers = sorted([int(getFileWithoutExtension(a)) for a in glob.glob(bankPath + larinPathPattern)], reverse=True)

    partedVariants = list(chunks(variantsNumbers, 4))

    for foury in partedVariants:
        variantsKeyboard.keyboard.append([dict(text='Вар.{}'.format(i)) for i in foury])

    return variantsKeyboard

###Ларин }