import msgpackrpc


display_text = r"""
 __          __     __                      _            _____          _____  
 \ \        / /    / _|                    | |          / ____|   /\   |  __ \ 
  \ \  /\  / /__  | |_ ___  _   _ _ __   __| |   __ _  | |       /  \  | |__) |
   \ \/  \/ / _ \ |  _/ _ \| | | | '_ \ / _` |  / _` | | |      / /\ \ |  _  / 
    \  /\  /  __/ | || (_) | |_| | | | | (_| | | (_| | | |____ / ____ \| | \ \ 
     \/  \/ \___| |_| \___/ \__,_|_| |_|\__,_|  \__,_|  \_____/_/    \_\_|  \_\ 

                      ___..............._
             __.. ' _'.""""""\\""""""""- .`-._
 ______.-'         (_) |      \\           ` \\`-. _
/_       --------------'-------\\---....______\\__`.`  -..___
| T      _.----._           Xxx|x...           |          _.._`--. _
| |    .' ..--.. `.         XXX|XXXXXXXXXxx==  |       .'.---..`.     -._
\_j   /  /  __  \  \        XXX|XXXXXXXXXXX==  |      / /  __  \ \        `-.
 _|  |  |  /  \  |  |       XXX|""'            |     / |  /  \  | |          |
|__\_j  |  \__/  |  L__________|_______________|_____j |  \__/  | L__________J
     `'\ \      / ./__________________________________\ \      / /___________\ 
     `.`----'.'   dp                                `.`----'.'
          `""""'                                         `""""'
"""

class FileServer(object):
    def push(self, result, timestamp):
    	if 'car' in result:
            print(display_text)
        return 'received {} bytes'.format(len(result))


# print(display_text)
server = msgpackrpc.Server(FileServer())
server.listen(msgpackrpc.Address('172.17.51.5', 18900))
print('start display service on 172.17.51.5:18900')
server.start()