class UniqObject:
    created = None
    
    @classmethod
    def create_object(cls):
        if cls.created is None:
            cls.created = UniqObject()
        return cls.created


if __name__ == '__main__':
    a = UniqObject.create_object()
    b = UniqObject.create_object()
    print(id(a))
    print(id(b))
