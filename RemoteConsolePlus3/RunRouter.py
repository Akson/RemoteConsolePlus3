'''Created by Dmytro Konobrytskyi, 2012(C)'''
from RCP3.Infrastructure.Router import Router

if __name__ == '__main__':
    print "Running router..."
    Router("tcp://*:55557", "tcp://*:55559").Run()
