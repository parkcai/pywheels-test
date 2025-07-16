import pywheels
from pywheels.miscellaneous import print_helloworld
from pywheels.miscellaneous import greet


def main():
    
    pywheels.set_language("en")
    
    print_helloworld()
    
    pywheels.init_language()
    
    greet("Jason Wei")
    
    
if __name__ == "__main__":
    
    main()
    
    
    