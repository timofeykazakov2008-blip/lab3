
class CatalogError(Exception):
    '''Базовая ошибка'''

class DublErrors(CatalogError):
    '''Ошибка при повторе индефикатора'''

class NonObjectErrors(CatalogError):
    '''Ошибка несуществующего объекта'''

class FileErrors(CatalogError):
    '''Ошибка загрузки и сохранения каталога'''

class ProductErrors(CatalogError):
    '''Ошибка данных продукта'''

class TimeErrors(CatalogError):
    '''Ошибка даты'''
