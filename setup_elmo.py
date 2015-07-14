#Create ELMO config


import logging
import sys
import time
import argparse

from test_cli.elmo import ElmoConnection
from test_cli.utils import getint


class ElmoSetup:
        '''Class container to hold Elmo configuration information and setup operations'''
        def __init__(self, host='192.168.1.2', gen=2, rate=1000000000, subport = 4, flows=[32,32,32,32], pktlen=1500, macda=True, macsa=False, dvlan=True):
        
                self.host = host
                self.gen = gen
                self.rate = rate
                self.subport = subport
                self.flows = flows
                self.pktlen = pktlen
                self.macda = macda
                self.macsa = macsa
                self.dvlan = dvlan

                
        def ElmoLogin(self):
                print("Connecting to ELMO at {host}...\n").format(host=self.host)
                cli = ElmoConnection(host=self.host, clear=True, clear_exit=True, logfile=True, loglevel=logging.DEBUG)
                print 'Logging to: {}\n'.format(cli.logfile)

                # Simple - execute command.
                cli.execute('show version', verbose=False)
                print cli.stdout # echo to console
                        
                return cli
                        
        def ElmoLogout(self):
                return
        
        
        def SetUpElmoFlows(self, cli):
                sub_num = 0
                flow_num = 0
                self.ClearAll(cli)
                self.SetPortRate(cli)
                self.SetGenRate(cli)

                #NEED A CHECK TO MAKE SURE NUMBER OF ITEMS IN SELF.FLOWS EQUALS NUMBER EXPECTED BY SELF.SUBPORT

                print "print macda: {macda}, macsa: {macsa}".format(macda=self.macda, macsa=self.macsa)

                while(sub_num < self.subport):
                        print "SUBPORT {sub_num}".format(sub_num=sub_num)
                        self.GenerateFlows(sub_num, flow_num, cli)
                        flow_num = flow_num + self.flows[sub_num]
                        sub_num = sub_num + 1
                        
                return

        def GenerateFlows(self, sub_num, flow_num, cli):
                totalFlows = flow_num + self.flows[sub_num]
                while(flow_num < totalFlows):
                        
                        self.MakeFlow(flow_num, cli)
                        
                        if self.macda:
                                self.SetMacda(flow_num, cli)
                        if self.macsa:
                                self.SetMacsa(flow_num, cli)
                        self.SetDvlan(sub_num, flow_num, cli)
                                
                        flow_num = flow_num + 1
                return

        def ClearAll(self, cli):
                print "Clearing all existing configurations"
                cli.execute('clear all force')
                return

        def SetPortRate(self, cli):
                print 'Configuring port {port}\n'.format(port=self.gen)
                cli.execute('set config port {port} rate 2'.format(port=self.gen))
                return

        def SetGenRate(self, cli):
                print 'Starting configuration on generator {gen}\n'.format(gen=self.gen)
                cli.execute('set config gen {gen} bitrate {rate}'.format(gen=self.gen, rate=self.rate))
                return
        
        
        def MakeFlow(self, flow_num, cli):
                print 'Establishing flow {flow_num}...\n'.format(flow_num=flow_num)
                cli.execute('set config gen {gen} flow {flow_num} lenmode Fixed lenmin {pktlen}'.format(gen=self.gen, flow_num=flow_num, pktlen=self.pktlen))
                
                
        def SetMacda(self, flow_num, cli):
                macda = self.MacGenerator(flow_num)
                cli.execute('set config gen {gen} flow {flow_num} macda {macda}'.format(gen=self.gen, flow_num=flow_num, macda=macda))
                return
                
                
        def SetMacsa(self, flow_num, cli):
                macsa = self.MacGenerator(flow_num)
                cli.execute('set config gen {gen} flow {flow_num} macsa {macsa}'.format(gen=self.gen, flow_num=flow_num, macsa=macsa))
                return
                
                
        def SetDvlan(self, sub_num, flow_num, cli):
                cli.execute('set config gen {gen} flow {flow_num} vlan1tpid x88a8 vlan1vid {vid1} vlan2tpid x8100 vlan2vid {vid2}'.format(gen=self.gen, flow_num=flow_num, vid1=sub_num, vid2=flow_num)) 
                return
                
        def MacGenerator(self, num):
                '''Takes a number from 0-4095, converts it to hex, 
                and formats the hex into the last 3 digits of a valid MAC address'''
                
                hex_num = str("{0:#0{1}x}".format(num,5))   #formats hex into 5 character string from 0x000 to 0xfff
                hex_string = hex_num.split('x')[1]          #chops the 0x of the front of 0xfff leaving fff
                
                mac_addr = "00:00:00:00:0{a}:{b}{c}".format(a=hex_string[0], b=hex_string[1], c=hex_string[2])
                
                return mac_addr
        

        
def GetInputs(elmo):
        
        parser = argparse.ArgumentParser(description='Get inputs to set up ELMO')
        parser.add_argument('--host', type=str, dest='host', help='The IP address of the Elmo device to configure')
        parser.add_argument('-g', '--gen', type=int, dest='gen', help='The number of the generator to create flows on (1-4)')
        parser.add_argument('-r', '-rate', type=int, dest='rate', help='The rate (in bits/second) of packet generation')
        parser.add_argument('-s', '--subport', type=int, dest='subport', help='The number of subports to create (inner tag of dvlan)')
        parser.add_argument('-f', '--flows', type=int, dest='flows', nargs='*', help='The number of flows to create on the generator listed out by subport.  Ex:  "-s 4 -f 500 100 10 1"  Note: Max flow number for Elmo2 is 1023')
        parser.add_argument('-p', '--pktlen', type=int, dest='pktlen', help='The packet size (in bytes) of each flow')
        parser.add_argument('--macda', dest='macda', action='store_true', help='Flag that if added sets a unique mac destination address for each flow')
        parser.add_argument('--macsa', dest='macsa', action='store_true', help='Flag that if added sets a unique mac source address for each flow')
        
        inputs = parser.parse_args()
        
        if inputs.host != None:
                elmo.host = inputs.host
        if inputs.gen != None:
                elmo.gen = inputs.gen
        if inputs.rate != None:
                elmo.rate = inputs.rate
        if inputs.subport != None:
                elmo.subport = inputs.subport
        if inputs.flows != None:
                elmo.flows = inputs.flows
        if inputs.pktlen != None:
                elmo.pktlen = inputs.pktlen
                
        return 0
        

def main():

        elmo = ElmoSetup()
        
        GetInputs(elmo)
        cli = elmo.ElmoLogin()
        elmo.SetUpElmoFlows(cli)
        elmo.ElmoLogout()

        return 0
        
main()
        
