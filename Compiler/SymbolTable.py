

class SymbolTable:

    def __init__(self):
        self.class_table = dict()
        self.subroutine_table = dict()
        self.index_class = dict()
        self.index_subroutine = dict()

    def startSubroutine(self):
        self.subroutine_table = dict()
        self.index_subroutine = dict()

    def define(self, name, type, kind, class_flag=False):
        if class_flag:
            self.varCount(kind, class_flag=True)
            self.subroutine_table[name] = (type, kind, self.index_class[kind])
        else:
            self.varCount(kind, class_flag=False)
            self.subroutine_table[name] = (type, kind, self.index_subroutine[kind])

    def varCount(self, kind, class_flag=False):
        if class_flag:
            self.index_class[kind] = self.index_class.get(kind, -1) + 1
        else:
            self.index_subroutine[kind] = self.index_subroutine.get(kind, -1) + 1

    def TypeOf(self, name):
        try:
            type = self.subroutine_table[name][0]
        except:
            type = self.class_table[name][0]
        return type

    def KindOf(self, name):
        try:
            kind = self.subroutine_table[name][1]
        except:
            kind = self.class_table[name][1]
        return kind

    def IndexOf(self, name):
        try:
            index = self.subroutine_table[name][2]
        except:
            index = self.class_table[name][2]
        return index
