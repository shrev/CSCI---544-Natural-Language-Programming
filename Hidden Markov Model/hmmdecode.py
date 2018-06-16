import sys
import cPickle as pickle
import math
import time

def viterbi(fpredict):	
	with open('hmmmodel.txt', 'rb') as handle:
		hmmmodel = pickle.load(handle)
	# print("--- %s seconds ---" % (time.time() - start_time))
	emission = hmmmodel[1]
	transition = hmmmodel[0]
	tc = hmmmodel[2]
	tps = hmmmodel[3]
	file = open(fpredict,"r")
	lines = file.readlines()
	file.close()
	count=0
	with open('hmmoutput.txt', 'wb') as output:
		# start_time = time.time()
		for line in lines:
			line =  line.replace('\n','')
			ll = line.split(' ')
			prev_tag =''
			prev_tags =[]
			chain =[]
			next_tags={}
			uc=0
			# for k in range(0,len(ll)):
			# 	if ll[k] not in emission:
			# 		uc+=1
			for k in range(0,len(ll)):
				if k==0: 
					prev_tags.append(('q',1,1))
				next_tags ={}
				em_tags =[]
				c=0
				# start_time = time.time()
				try:
					for l in emission[ll[k].lower()] :
							c =1
							for bcp in prev_tags:
								tsition = transition[bcp[0]][l]
								val = emission[ll[k].lower()][l]+bcp[1]+tsition
								if l in next_tags:
									if(next_tags[l][0]<val):
										next_tags[l] = (val,bcp[0])
								else:
									next_tags[l] = (val,bcp[0])
				except KeyError:
					maxp=(0,-1,0)
					for bcp in prev_tags:
					# 	if maxp[1]<bcp[1]:
					# 		maxp=bcp
					# maxev = 0
						for l in transition[bcp[0]]:
								# if em[1]>maxev:
								val = transition[bcp[0]][l]+bcp[1]
								if l in next_tags:
									if l=='NN':
										val = val+1
									if next_tags[l][0]<(val) :
										next_tags[l] = (val,bcp[0])
								else :
									next_tags[l] = (val,bcp[0])
									# maxev = em[1]
					# print ll[k]+" "+tag[0][1]
				chain.extend(prev_tags)
				# print ("chain",chain)
				# print ("prev_tags",prev_tags)
				# if ll[k].lower() in emission:
				#  print ("em_tags",emission[ll[k].lower()])
				# else :
				# 	print ("em_tags",[])
				# print ("next_tags",next_tags)
				# print ("next_tags",max(next_tags,key=lambda item:next_tags[item]))
				prev_tags = [(l,v[0],v[1]) for l,v in next_tags.items()]
			# count =count+1
			# print count
			p =  max(prev_tags,key=lambda item:item[1])
			chain.append(p)
			# print chain
			last_tag = chain[-1][2]
			rll = ll[::-1]
			o = 0
			rll[o] = rll[o]+'/'+chain[-1][0]
			chain = chain[:len(chain)-1]
			while o<len(rll)-1:
				o=o+1
				temp=""
				for x in reversed(chain):
					if x[0]==last_tag :
				 		temp = x
				 		break
				rll[o] = rll[o]+'/'+temp[0]
				# print rll[o]
				last_tag=temp[2]
				chain =  chain[:len(chain)-tc]
				# print chain
			output.write((' ').join(rll[::-1])+'\n')
			# stop_time = time.time()
			print("--- %s seconds ---" % (time.time() - start_time))
			


if __name__ == "__main__":
    start_time = time.time()
    arg1 = sys.argv[1]
    viterbi(arg1)
    print("--- %s seconds ---" % (time.time() - start_time))
							

						






