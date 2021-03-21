

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
            index = self.varCount(kind, class_flag=True) + 1
            self.subroutine_table[name] = (type, kind, index)
        else:
            index = self.varCount(kind, class_flag=False) + 1
            self.subroutine_table[name] = (type, kind, index)

    def varCount(self, kind, class_flag=False):
        if class_flag:
            return self.index_class.get(kind, -1)
        else:
            return self.index_subroutine.get(kind, -1)

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
