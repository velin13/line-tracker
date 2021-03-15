def Singleton(cls):
    """ Restrict instantiation of a class to one object. """
    instance = {}
    
    def getInstance(*args, **kwargs):
        """ Return instance """
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return getInstance
