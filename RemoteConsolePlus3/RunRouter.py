'''Created by Dmytro Konobrytskyi, 2012(C)'''
from RCP3.Infrastructure.Router import Router
import traceback

if __name__ == '__main__':
    try:
        Router("tcp://*:55557", "tcp://*:55559").Run()
    except:
        print traceback.format_exc()
        print "Probably another router is already running."
