

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

    def TypeOf(self, name, class_flag=False):
        if class_flag:
            self.class_table[name][0]
        else:
            self.subroutine_table[name][0]

    def KindOf(self, name, class_flag=False):
        if class_flag:
            self.class_table[name][1]
        else:
            self.subroutine_table[name][1]

    def IndexOf(self, name, class_flag=False):
        if class_flag:
            self.class_table[name][2]
        else:
            self.subroutine_table[name][2]
