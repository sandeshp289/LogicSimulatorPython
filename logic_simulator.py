#/////////////////////////////////////////////////////////////////////////////////////
#// File       : logic_simulator.py
#// Language   : Python
#// Description: Event-Driven Combinational/Sequential Logic Simulator
#// Author     : Sandesh Prabhakar
#// Created    : November 9, 2025
#// Modified   : August 15, 2026
#// Version    : 1.0
#//
#// Copyright (c) 2026 Sandesh Prabhakar
#// All rights reserved
#//////////////////////////////////////////////////////////////////////////////////////

import sys
import numpy as np
from enum import Enum

def evaluate (j, gtype, value, vec, pso, fanin, faninlist ):
	match gtype[j]:
		#INPUT
		case 1:
			value[j]=vec[j]

		#PSEUDO INPUT PSI
		case 14:
			value[j]=value[int(pso[j])]


		#PSEUDO OUTPUT PSO
		case 15:
			value[j]=value[int(faninlist[j][0])]

		#NAND gate
		case 7:
			out='0'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '0':
					value[j]='1'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out 

		#AND gate
		case 6:
			out='1'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '0':
					value[j]='0'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out

		#OR gate
		case 8:
			out='0'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '1':
					value[j]='1'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out

		#NOR gate
		case 9:
			out='1'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '1':
					value[j]='0'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out

		#XOR gate
		case 3:
			out_int=0;
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == 'X':
					value[j]='X'
					return
				elif value[int(faninlist[j][nn])] == '1':
					out_int=not out_int

				match out_int:
					case 0:
						out = '0'
					case 1:
						out = '1'
				value[j]=out

		#XNOR gate
		case 4:
			out_int=0;
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == 'X':
					value[j]='X'
					return
				elif value[int(faninlist[j][nn])] == '1':
					out_int=not out_int

				match out_int:
					case 0:
						out = '1'
					case 1: 
							out = '0'
				value[j]=out 

		#NOT gate
		case 10:
			if value[int(faninlist[j][0])] == '0':
				value[j]='1'
			elif value[int(faninlist[j][0])] == '1':
				value[j]='0'
			elif value[int(faninlist[j][0])] == 'X':
				value[j]='X'

		#BUF gate
		case 11:
			value[j]=value[int(faninlist[j][0])]

		#TIE_1
		case 12:
			value[j]='1'

		#TIE_0
		case 13:
			value[j] = '0'

		#OUTPUT
		case 2:
			value[j]=value[int(faninlist[j][0])]

		#D_FF
		case 5:
			value[j]=value[int(faninlist[j][0])]
				
class Gate(Enum):
	G_JUNK   =  0
	G_INPUT  =  1
	G_OUTPUT =  2
	G_XOR    =  3
	G_XNOR   =  4
	G_DFF    =  5
	G_AND    =  6
	G_NAND   =  7
	G_OR	 =  8
	G_NOR    =  9
	G_NOT    =  10
	G_BUF    =  11
	G_TIE1   =  12
	G_TIE0   =  13
	G_PSI    =  14
	G_PSO    =  15

lev_file=sys.argv[1] + ".lev"
vec_file=sys.argv[1] + ".vec"

try:
	with open(lev_file, "r") as file:
		content = file.read()
		print("File",lev_file," found")
		#print(content)
except FileNotFoundError:
	print("Error: The file ",lev_file," was not found.")

try:
	with open(vec_file, "r") as file:
		content = file.read()
		print("File",vec_file," found")
		#print(content)
except FileNotFoundError:
	print("Error: The file ",vec_file," was not found.")

line_number=0
gate_count=0
numInputs=0
numOutputs=0
numDFFs=0
maxlevels=0
numgates=0
numPSIs=0
numPSOs=0
with open(lev_file, "r") as f:
	for line in f:
		line_number=line_number+1
		# Assuming space-separated values
		parts = line.split() 
		if line_number==1:
			count=int(parts[0])
			gate_count=count-1
			gtype=np.empty(count*2)
			fanin=np.empty(count*2)
			fanout=np.empty(count*2)
			levelNum=np.empty(count*2)
			dff=np.empty(count)
			pout=np.empty(count)
			faninlist=np.empty((count*2,count))
			fanoutlist=np.empty((count*2,count))
			gate_at_level=np.empty((5000,count*2))
			EventList=np.empty((5000,count*2))
			num_gate_per_level=np.zeros(5000,dtype=int)
			pso=np.empty(count)
			value=np.empty(count*2,dtype=object)
			psi_list=np.empty(count)
			pso_list=np.empty(count)

			
		if line_number>2:
			if line_number < count+2:
				numgates += 1
				gatenum=int(parts[0])
				f1=int(parts[1])
				f2=int(parts[2])
				f3=int(parts[3])

				gtype[gatenum]=f1
				if gtype[gatenum] > 13:
					print("gate ",gatenum," is an unimplemented gate type")
				elif gtype[gatenum] == Gate.G_INPUT.value :
					numInputs += 1
				elif gtype[gatenum] == Gate.G_OUTPUT.value :
					numOutputs += 1
					pout[numOutputs]=gatenum
				elif gtype[gatenum] == Gate.G_DFF.value :
					numDFFs += 1
					dff[numDFFs]=gatenum


				#levenNum[gatenum]= (f2+5)/5;
				levelNum[gatenum] = f2

				if f2 >= maxlevels:
					maxlevels=f2 + 5; 

				fanin[gatenum]=f3

				f4=int(parts[3+(2*f3)+1])
				fanout[gatenum]=f4

total_levels = int(maxlevels/5)

line_number=0		
numDFFs=0
numInputs=0
numOutputs=0
with open(lev_file, "r") as f:
	for line in f:
		line_number=line_number+1
		# Assuming space-separated values
		parts = line.split() 

		if line_number>2:
			if line_number < count+2:
				gatenum=int(parts[0])
				f1=int(parts[1])
				f2=int(parts[2])
				f3=int(parts[3])
				gtype[gatenum]=f1
				if gtype[gatenum] > 13:
					print("gate ",gatenum," is an unimplemented gate type")
				elif gtype[gatenum] == Gate.G_INPUT.value :
					numInputs += 1
				elif gtype[gatenum] == Gate.G_OUTPUT.value :
					numOutputs += 1
					pout[numOutputs]=gatenum
				elif gtype[gatenum] == Gate.G_DFF.value :
					numDFFs += 1
					dff[numDFFs]=gatenum
					gtype[gatenum]= Gate.G_PSI.value
					numPSIs += 1
					psi_list[numPSIs]=gatenum
					gtype[count-1+numDFFs]= Gate.G_PSO.value
					numPSOs +=1
					pso_list[numPSOs]=count-1+numDFFs 
					pso[gatenum]=count-1+numDFFs


				#levenNum[gatenum]= (f2+5)/5;
				levelNum[gatenum] = f2
				levelNum[count-1+numDFFs] = int(maxlevels-5)


				if gtype[gatenum]==Gate.G_PSI.value:
					num_gate_per_level[f2] = num_gate_per_level[f2] + 1
					num_gate_per_level[int(maxlevels-5)] = num_gate_per_level[int(maxlevels-5)] + 1
					gate_at_level[f2][num_gate_per_level[f2]] = gatenum;
					gate_at_level[int(maxlevels-5)][num_gate_per_level[int(maxlevels-5)]] = count-1+numDFFs;
					fanin[gatenum]=0
					fanin[count-1+numDFFs]=f3
					f4=int(parts[3+(2*f3)+1])
					fanout[gatenum]=f4
					fanout[count-1+numDFFs]=0
							
					for i in range(0,f3):
						faninlist[count-1+numDFFs][i]=int(parts[3+(i+1)])
			
					for i in range(0,f4):
						fanoutlist[gatenum][i]=int(parts[3+(2*f3)+1+(i+1)])

					value[gatenum]='X'
					value[count-1+numDFFs]='X'


				
				else:
					num_gate_per_level[f2] = num_gate_per_level[f2] + 1
					gate_at_level[f2][num_gate_per_level[f2]] = gatenum;
					fanin[gatenum]=f3
					f4=int(parts[3+(2*f3)+1])
					fanout[gatenum]=f4

					for i in range(0,f3):
						faninlist[gatenum][i]=int(parts[3+(i+1)])
			
					for i in range(0,f4):
						fanoutlist[gatenum][i]=int(parts[3+(2*f3)+1+(i+1)])

					value[gatenum]='X'

print("Successfully read in circuit:")
print(numInputs," PIs.")
print(numOutputs," POs.")
print(numDFFs," DFFs.")
print(numgates," total number of gates.")
print(total_levels," levels in the circuit.")
print("\n")


polevel = int(maxlevels -5)

line_number=0		
with open(vec_file, "r") as f:
	for line in f:
		line_number=line_number+1
		# Assuming space-separated values
		parts = line.split() 

		if line_number==1:
			count=int(parts[0])
			vec=np.empty(count+2,dtype=object)
		if line_number>1 and parts[0]!= 'END':
			input_string=parts[0]	
			print("Input Vector  ",line_number-2,": ",input_string) 
			i=0
			for bit in input_string:
				i += 1	
				vec[i]=bit
			
			for i in range(0,maxlevels,5):
				for js in range(1,num_gate_per_level[i]+1):
					j=int(gate_at_level[i][js])
					if levelNum[j]==i and (i==0 or i==polevel):
						EventList[i][j]=j
					else:
						EventList[i][j]=0


			for i in range(0,maxlevels,5):
				for js in range(1,num_gate_per_level[i]+1):
					j=int(gate_at_level[i][js])
					if EventList[i][j]==j:
						temp=value[j]
						evaluate(j, gtype, value, vec, pso, fanin, faninlist )

						if temp==value[j]:
							for kk in range(0,int(fanout[j])):
								h=int(fanoutlist[j][kk])
								r=int(levelNum[h])
								if EventList[r][h]==h:
									break
								else:
									EventList[r][h]=0
						else:
							for kk in range(0,int(fanout[j])):
								h=int(fanoutlist[j][kk])
								r=int(levelNum[h])
								EventList[r][h]=h

			#Printing out the Primary output values corresponding to each vector

			print("Output Vector  ",line_number-2," : ",end="")
			for zz in range (1,numOutputs+1):
				print(value[int(pout[zz])],end="")

			print("\n")

			if numDFFs>0:
				for zz in range(1,numDFFs+1):
					print(value[int(psi_list[zz])],end="")
				print("\n")

		#print("\n")

#If it is a sequential circuit containing D F/Fs, the following section section will also get executed
if numDFFs > 0:
	print("Final Next State")
	for zz in range(1,numDFFs+1):
		print(value[int(pso_list[zz])],end="")
	print("\n")

print("Total number of patterns is ", line_number-2)
