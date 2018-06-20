
from model.exceptions import OperationNotAllowedException
from model.BaseBL import BaseBL
from model.TocDAL import TocDAL

class TocBL(BaseBL):

    
    @staticmethod
    def delete(context, id):
        if not TocBL._deleteAllowed(context, id):
            raise OperationNotAllowedException(id)
        TocBL._preDelete(context, id)
        TocDAL.delete(context, id)   
        TocBL._postDelete(context, id)
        
    @staticmethod
    def insert(context, entity):
        if not TocBL._insertAllowed(context, id):
            raise OperationNotAllowedException(id)
        TocBL._preInsert(context, entity)
        TocDAL.insert(context, entity)   
        TocBL._postInsert(context, entity)     
        
    @staticmethod
    def read(context, id):
        if not TocBL._readAllowed(context, id):
            raise OperationNotAllowedException(id)        
        TocBL._preRead(context, id)
        TocDAL.read(context, id)   
        TocBL._postRead(context, id)   

    @staticmethod
    def update(context, entity):
        if not TocBL._updateAllowed(context, id):
            raise OperationNotAllowedException(id) 
        TocBL._preUpdate(context, entity)
        TocDAL.update(context, entity)   
        TocBL._postUpdate(context, entity)    

    @staticmethod
    def _recogerAllowed(context, entity):
        return True
    
    @staticmethod
    def _recogerImpl(context, entity):
        pass

    @staticmethod
    def recoger(context, entity):        
        if not TocBL._recogerAllowed:
            raise OperationNotAllowedException(id)
        TocBL._recogerImpl(context, entity)
            
    