def compileCommands(commandvar):
    try:
        return eval(commandvar), False
    except Exception as e:
        return [], e
