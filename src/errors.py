
class CatalogError(Exception):
    '''Базовая ошибка'''

class FileErrors(CatalogError):
    '''Ошибка загрузки и сохранения каталога'''

class ProductErrors(CatalogError):
    '''Ошибка данных продукта'''

class TimeErrors(CatalogError):
    '''Ошибка даты'''
