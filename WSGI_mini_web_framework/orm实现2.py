# 定义一个modelmetaclass类继承元类(type)
class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        # 定义一个字典
        mappings=dict()
        # 判断是否需要保存
        for k,v in attrs.items():
            # 判断是否是指定的StringField和IntegerField的实例对象
            if isinstance(v,tuple):
                #print("Founding mapping:%s ==>%s" %(k,v))
                mappings[k]=v
        # 删除这些已经在字典中存储的属性
        for k in mappings.keys():
            attrs.pop(k)

        # 将之前的uid/name/email/passward以及对应的对象引用，类名字
        attrs["__mappings__"]=mappings  # 保存属性和列的映射关系
        attrs["__table__"]=name # 假设表名和类一致
        return type.__new__(cls,name,bases,attrs)


class model(object,metaclass=ModelMetaclass):
    # 当指定元类之后，以上的类属性就不在类中，而是在__mappings__属性指定的字典中存储
    # 以上User类中有：
    # __mappings__ = {
    #     "uid": ("uid","int unsigned")
    #     "name": ("username","varchar(30)")
    #     "email":("email","varchar(30)")
    #     "passward":("passward","varchar(30)")
    # }
    # __table__="User"
    #定义__init__方法
    def __init__(self,**kwargs):
        for name,value in kwargs.items():
            setattr(self,name,value)

    def save(self):
        fields=[]
        args=[]
        for k,v in self.__mappings__.items():
            fields.append(k)
            args.append(getattr(self,k,None))

            #sql="insert into %s (%s) value (%s)" % (self.__table__,",".join(fields), ",".join([str(i) for i in args]))
            # 完善对数据类型的检测
        args_temp=list()
        for temp in args:
            if isinstance(temp,int):
                args_temp.append(str(temp))
            elif isinstance(temp,str):
                args_temp.append("""'%s'""" % temp)

        sql="insert into %s (%s) values (%s)" % (self.__table__, ','.join(fields), ','.join(args_temp))
        print("SQL: %s" % sql)


# 定义一个user类继承元类(modelmetaclass)
class User(model):
    uid=("uid","int unsigned")
    name=("username","varchar(30)")
    email=("email","varchar(30)")
    passward=("passward","varchar(30)")


u = User(uid=123456, name="xxxx", email="xxxx@qq.com", passward="xxxxx")
u.save()
u = User(uid=1234567, name="fhl", email="2546374141@qq.com", passward="xxxxxxxxxxx")
u.save()








