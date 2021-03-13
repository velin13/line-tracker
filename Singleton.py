def Singleton(cls):
    instance = {}
    
    def getInstance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return getInstance
