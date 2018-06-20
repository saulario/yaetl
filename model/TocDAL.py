
class TocDAL():
    
    @staticmethod
    def delete(context, id):
        print("TocDAL.delete")
    
    @staticmethod
    def insert(context, obj):
        print("TocDAL.insert")
        return obj;
    
    @staticmethod
    def read(context, id):
        print("TocDAL.read")
        obj = {}
        return obj;
    
    @staticmethod
    def update(context, obj):
        print("TocDAL.update")
        return obj