

class SymbolTable:

    def __init__(self):
        self.class_table = dict()
        self.subroutine_table = dict()
        self.index_class = dict()
        self.index_subroutine = dict()

    def startSubroutine(self):
        """Reset subroutine table."""
        self.subroutine_table = dict()
        self.index_subroutine = dict()

    def define(self, name, type, kind, class_flag=False):
        """Define an entry in one of the the tables."""
        if class_flag:
            index = self.varCount(kind, class_flag=True)
            self.index_class[kind] = index
            self.class_table[name] = (type, kind, index)
        else:
            index = self.varCount(kind, class_flag=False)
            self.index_subroutine[kind] = index
            self.subroutine_table[name] = (type, kind, index)

    def varCount(self, kind, class_flag=False):
        """Return the count of a kind."""
        if class_flag:
            index = self.index_class.get(kind, -1) + 1
        else:
            index = self.index_subroutine.get(kind, -1) + 1
        return index

    def TypeOf(self, name):
        """Return the type of an entry."""
        try:
            type = self.subroutine_table[name][0]
        except:
            try:
                type = self.class_table[name][0]
            except:
                type = name
        return type

    def KindOf(self, name):
        """Return the kind of an entry."""
        try:
            kind = self.subroutine_table[name][1]
        except:
            try:
                kind = self.class_table[name][1]
            except:
                kind = None
        return kind

    def IndexOf(self, name):
        """Return the index of an entry."""
        try:
            index = self.subroutine_table[name][2]
        except:
            index = self.class_table[name][2]
        return index
