import pywheels
from pywheels.miscellaneous import print_helloworld
from pywheels.miscellaneous import greet


def main():
    
    print_helloworld()
    greet("Jason Wei")
    
    pywheels.set_language("en")
    
    print_helloworld()
    greet("Jason Wei")
    
    pywheels.init_language()
    
    print_helloworld()
    greet("Jason Wei")
    
    
if __name__ == "__main__":
    
    main()
    
    
    