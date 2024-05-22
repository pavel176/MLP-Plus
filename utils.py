from log import error

def split(delimiter, text):
    blocks = []
    text_block = ""
    for symbol in text:
        if symbol in delimiter:
            if text_block != "":
                blocks.append(text_block)
                text_block = ""
            blocks.append(symbol)
        else:
            text_block += symbol

    if text_block != "":
        blocks.append(text_block)

    return blocks

def split_save_text(delimiter, delimiter_text, text):
    blocks = []
    text_block = ""
    is_text = False
    open_text = ""
    for symbol in text:
        if symbol in delimiter_text:
            if is_text and symbol == open_text:
                is_text = False
                open_text = ""
                text_block += symbol
                blocks.append(text_block)
                text_block = ""
            else:
                open_text = symbol
                is_text = True
                text_block += symbol
        elif symbol in delimiter:
            if text_block != "":
                blocks.append(text_block)
                text_block = ""
            blocks.append(symbol)
        else:
            text_block += symbol

    if text_block != "":
        blocks.append(text_block)

    if is_text:
        error("[SyntaxError] The text was not closed")

    return blocks

def index_line_in_arr(arr: list[str], text: str) -> int:
    for i in range(len(arr)):
        if text in arr[i]:
            return i
    return -1


def split_array(arr: list[str], delimiter: str) -> list[list[str]]:
    blocks = []
    arr_block = []
    for text in arr:
        if text == delimiter:
            blocks.append(arr_block)
            arr_block = []
        else:
            arr_block.append(text)

    blocks.append(arr_block)

    return blocks

def join(arr: list[str], delimiter = ""):
    text = ""
    if len(arr) < 1:
        error("[Utils.join] Length list < 1")
    if len(arr) > 1:
        for i in arr[:-1:]:
            text += i + delimiter
    return text + arr[-1]

def D_PrintedFunction(text):
    def my_decorator(func):
        def wrapped(self=None):
            print("="*20)
            print(f"{text}:")
            if self != None:
                func(self)
            else:
                func()
            print("="*20)
        return wrapped
    return my_decorator

def assembler_insert(assemler, insert_assembler, index):
    if len(assemler) == 0:
        return insert_assembler
    else:
        start = []
        end = []
        if index < 0:
            index = -index - 1
        if index == 0:
            end = assemler
        elif index == len(assemler) - 1:
            start = assemler
        else:
            start = assemler[:index:]
            end = assemler[index::]
        return start + insert_assembler + end

def no_tab(stroke: list[str]):
    return list(filter(lambda text: text != "\t", stroke))

def replace_arr(arr: list[str], old: str, new: str) -> list[str]:
    new_arr = []
    for i in arr:
        if i == old:
            new_arr.append(new)
        else:
            new_arr.append(i)
    return new_arr