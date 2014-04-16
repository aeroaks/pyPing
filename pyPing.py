'''
USE linux's ping command to calculate network latency, jitter and packet loss within 
python.
host = "www.google.com"

#create a process
ping = subprocess.Popen(["ping", "-c", "4", host], stdout = subprocess.PIPE,stderr = subprocess.PIPE)

# interacrt with process
out, error = ping.communicate()

# output
print out
'''

import sys, subprocess, statistics

def main(hostName):
    
    '''
    Runs when the program is called from command line
    '''
    
    try:
        pktNum = int(input("Enter desired number of packets: "))
    except ValueError:
        print ("Not a valid number. '3' selected")
        pktNum = "3"
    
    try:
        pktSize = int(input("Enter desired packet size: "))
    except ValueError:
        print ("Not a valid number. '56' selected")
        pktSize = "56"
        
    #create a process
    ping = subprocess.Popen(['ping','-s',str(pktSize),'-c',str(pktNum), hostName], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
    # interacrt with process
    out, error = ping.communicate()

    # show output
    #~ print (error.decode("UTF-8"))
    #~ print (out.decode("UTF-8"))
    # extract output details
    parsePing(out)
    
    
def parsePing(outTxt):
    """
    parse the ping output and get parameters
    """
    timeLst = []
    for line in outTxt.decode("UTF-8").splitlines():
        timePos = line.find('time=')
        pktPos = line.find('packets trans')
        
        if timePos > 0:
            """
            parsing time val
            """
            timeVal = float(line[line.find('=',timePos)+1:line.find('ms')])
            timeLst.append(timeVal) 
        
        if pktPos > 0:
            """
            parsing packet loss information
            """
            pktTx = int(line[:pktPos])
            pktRx = int(line[line.find(',')+1:line.find('rece')])
            if pktRx == 0:
                print(line.find(',',int(line.find('%'))-5)+1,line.find('%'),line[line.find(',',int(line.find('%'))-5)+1:line.find('%')])
                pktLoss = int(line[line.find(',',int(line.find('%'))-5)+1:line.find('%')])
            else:
                pktLoss = int(line[line.find(',',int(line.find('ved,')))+1:int(line.find('%'))])
            
            print ("Packet \n Tx: %d \t Rx: %d \t Loss: %d" % (pktTx,pktRx,pktLoss))

    if len(timeLst) > 0:
        """
        calculate time values : Latency and Jitter
        """
        timeMin = min(timeLst)
        timeMax = max(timeLst)
        timeTotal = sum(timeLst)
        timeAvg = timeTotal/len(timeLst)
        timeVar = statistics.variance(timeLst)
        
        print ("Time (ms) \n Min: %.1f \t Max: %.1f \n Latency(Avg): %.1f \n Jitter: %.2f" % (timeMin, timeMax, timeAvg, timeVar))


if __name__ == '__main__':
    values = sys.argv
    if len(values) == 1:
        main('www.google.com')
    else:
	# takes the IP/URL given in the command line argument as input
        main(values[1])
