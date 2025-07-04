"""

This file is intended to be hooked up to a computer (Raspberry pi in this case) that's hooked up directly to the arduino running the Sous Vide machine; it acquires data and writes it out to

sous_videslog.pickle

"""

import serial
import time
import pickle
import matplotlib.pyplot as plt

try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
except:
    ser = serial.Serial('COM3', 9600)    
ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)
import pdb
#if len(ans)=0


#work on more gracefully handling errors.
#any possible restart script (communicate previous state back)? Data Logging.
savedataevery = 5.0
cur_time = []
cur_temp = []
cur_sp = []
cur_p = []
cur_i = []
cur_d = []
cur_val = []
last_time = -1000.
print 'yay'
#fig = plt.figure(1)
#ax = fig.add_subplot(111)
#fig2 = plt.figure(2)
#ax2 = fig2.add_subplot(111)
#plt.ion()
#plt.show()
if __name__=='__main__':
    try:
        buffer1 = ''
        count = 0
        while True:
            st = ser.readline()
            buffer1 = st
            count+=1
    #        print st
            if True:#st == '\r' or st=='\n':
                #st = ser.read()
                #print buffer1
                ans = buffer1.split(',')
                #print len(ans), ans
                if len(ans)>6:
                    #print float(ans[0]) - last_time
                    if float(ans[0]) - last_time > savedataevery:
                        try:
                            [float(i) for i in ans[:7]]
                            cur_time.append(float(ans[0]))
                            cur_temp.append(float(ans[1]))
                            cur_sp.append(float(ans[2]))
                            cur_p.append(float(ans[3]))
                            cur_i.append(float(ans[4]))
                            cur_d.append(float(ans[5]))
                            cur_val.append(float(ans[6]))
                            last_time = cur_time[-1]
    #                        import pdb
    #                        pdb.set_trace()
                            # ax.plot(cur_time, cur_temp, 'kx-')
                            # ax.plot(cur_time, cur_sp, 'rx-')
                            # ax2.plot(cur_time, cur_p, 'kx-')
                            # ax2.plot(cur_time, cur_i, 'rx-')
                            # ax2.plot(cur_time, cur_d, 'bx-')
                            # ax2.plot(cur_time, cur_val, 'gx-')
                            # plt.draw()
                            print cur_time[-1], cur_temp[-1], cur_sp[-1], cur_p[-1], cur_i[-1], cur_d[-1], cur_val[-1]
                            pickle.dump([cur_time, cur_temp, cur_sp, cur_p, cur_i, cur_d, cur_val], open('sous_videslog.pickle','w'))
                        except:
                            pass #if there's an error, try again next time
                        
                buffer1=''
            else:
                buffer1+=st
                #print buffer1
            time.sleep(0.1)
    except:
        print "ERROR"
        import sys
        print sys.exc_info()
#        import pdb
#        pdb.set_trace()
    finally:

        ser.close()


#        print 'rasp' + buffer1
