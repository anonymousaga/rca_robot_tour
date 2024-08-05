def compileCommands(commandvar):
    commandvar = commandvar.strip().splitlines()
    command2 = []
    try:
        for x in commandvar:
            if x=="u":
                command2.append((1,180))
            elif x=="-u":
                command2.append((1,-180))
            elif x=="l":
                command2.append((1,-90))
            elif x=="r":
                command2.append((1,90))
            elif x=="rd":
                command2.append((1,45))
            elif x=="ld":
                command2.append((1,-45))
            elif x.startswith("sd"):
                command2.append((0,float(x.strip("sd"))*1.414))
            elif x.startswith("s"):
                command2.append((0,float(x.strip("s"))))
            elif x.startswith("t"):
                command2.append((1,float(x.strip("t"))))
            elif x.strip()=="":
                pass # skip blank lines
            else:
                raise ValueError('command is incorrect')
        return command2, False
    except ValueError as e:
        return [], e
