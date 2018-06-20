
class BaseBL():
    
    @staticmethod
    def _preDelete(context, id):
        print("BaseBL._preDelete")
    
    @staticmethod
    def _postDelete(context, id):
        print("BaseBL._postDelete")
        
    @staticmethod
    def _deleteAllowed(context, id):
        return True
        
    @staticmethod
    def _preInsert(context, obj):
        print("BaseBL._preInsert")
    
    @staticmethod
    def _postInsert(context, obj):
        print("BaseBL._postInsert")
        
    @staticmethod
    def _insertAllowed(context, obj):
        return True
        
    @staticmethod
    def _preRead(context, id):
        print("BaseBL._preRead")
        
    @staticmethod
    def _postRead(context, id):
        print("BaseBL._postRead")
        
    @staticmethod
    def _readAllowed(context, id):
        return True        
        
    @staticmethod
    def _preUpdate(context, obj):
        print("BaseBL._preUpdate")       

    @staticmethod
    def _postUpdate(context, obj):
        print("BaseBL._postUpdate")

    @staticmethod
    def _updateAllowed(context, obj):
        return True  