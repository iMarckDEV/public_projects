PASSWORD='1020'

#definir una funcion dentro de otra funcion
def pass_required(func):
    def wrapper():
        passw= input('input pass:>>')
        if passw == PASSWORD:
            return func() ###llamar con ()
        else:
            return 'la pass no es correcta'
    return wrapper


##la forma de usar los decoradores es con @ y se colocan encima de la funcion
@pass_required
def needs_password():
   return 'la pass es correcta'

def upper(func):
    def wrapper(*args,**kargs):
        #* o ** son una expansion
        result=func(*args,**kargs)

        return result.upper()

    return wrapper

@upper
def say_my_name(name):
    #print(f'hola {name}')
    return f'hola {name}'
if __name__=='__main__':
    #needs_password()
    print(say_my_name('imarck.dev'))
    needs_password_result = needs_password()  # Call the decorated function
    print(needs_password_result)