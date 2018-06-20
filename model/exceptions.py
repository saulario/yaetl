
class OperationNotAllowedException(RuntimeError):
    msg = None   
    def __init__(self, msg):
        super.__init__(msg)
        
class IllegalStateException(RuntimeError):
    msg = None   
    def __init__(self, msg):
        super.__init__(msg)        