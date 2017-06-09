import os
os.system('systemctl start mariadb')
os.system('redis-server')
os.system('python encoder.py>encoderlog')
os.system('python decoder.py>decoderlog')
os.system('python smip.py>smiplog')
os.system('python ivp.py>ivplog')
