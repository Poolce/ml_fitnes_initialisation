import source.select.generation as generator


def GenNSelectObj(n):
    Result = []
    while (n > 0):
        sel = generator.SelectUsingParams()
        if (sel.Fitnes > -1):
            Result.append(sel)
            n -= 1
    return Result


def CompairNSelectObj(objects):
    Result = []
    for leftObj in objects:
        for rightObj in objects:
            if (leftObj.Fitnes == rightObj.Fitnes):
                continue
            CompairOBJ = generator.Compair(leftObj, rightObj)
            Result.append(CompairOBJ)
    return Result
