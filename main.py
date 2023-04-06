import source.selection as sel


def main():
    Fitness = sel.GenNSelectObj(10)
    Selection = sel.CompairNSelectObj(Fitness)
    for i in Selection:
        print(i.Classification, " ", i.leftSel.Fitnes, " ", i.rightSel.Fitnes)


if (__name__ == "__main__"):
    main()
