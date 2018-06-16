import sys
import cPickle as pickle
import math
import time


def readTrain(ftrain):
	emission ={}
	emission_num={}
	transition_num = {}
	transition_num['q'] ={}
	transition ={}
	tag_counts ={}
	word_counts={}
	wc=0
	file = open(ftrain,"r")
	text = file.readlines()
	for line in text:
		line  = line.replace('\n','')
		ll = line.split(' ')
		for i in range(0,len(ll)):
			tag = ll[i].split('/')[-1]
			string = ll[i].split('/'+tag)[0]
			if string.lower() in word_counts:
				word_counts[string.lower()]= word_counts[string.lower()]+1
			else:
				word_counts[string.lower()]= 1
			if string.lower() in emission_num:
				if tag in emission_num[string.lower()] :
					emission_num[string.lower()][tag] = emission_num[string.lower()][tag]+1
				else:
					emission_num[string.lower()][tag] =1
			else:
				emission_num[string.lower()]={}
				emission_num[string.lower()][tag] = 1
			if i==0:
				tag = ll[i].split('/')[-1]
				if tag in transition_num['q'] :
					transition_num['q'][tag] = transition_num['q'][tag]+1
				else:
					transition_num['q'][tag] = 1			
			if i+1 <len(ll):
				tag_first = ll[i].split('/')[-1]
				tag_next = ll[i+1].split('/')[-1]
				if tag_first in tag_counts :
					tag_counts[tag_first] = tag_counts[tag_first]+1
				else :
					tag_counts[tag_first]=1
				if tag_first in transition_num :
					if tag_next in transition_num[tag_first]:
						transition_num[tag_first][tag_next] = transition_num[tag_first][tag_next]+1
					else:
						transition_num[tag_first][tag_next] = {}
						transition_num[tag_first][tag_next] = 1
				else:
					transition_num[tag_first]={}
					transition_num[tag_first][tag_next] = {}
					transition_num[tag_first][tag_next] = 1
			else:
				tag = ll[i].split('/')[-1]
				if tag in tag_counts :
					tag_counts[tag] = tag_counts[tag]+1
				else :
					tag_counts[tag]=1
	tags = tag_counts.keys()
	notags = sum(tag_counts.values())
	nowords = sum(word_counts.values())
	tps = {}
	unknown={}
	tagsf = ['q'] + tags
	ld =0.9
	wd=0.99
	tc = len(tag_counts)
	qc=0
	for ntag in tags:
		for ptag in tagsf:
			if ptag=='q':
				qc +=1
			if ptag not in transition:
				transition[ptag]={}
			if ptag in transition_num:
				if ntag in transition_num[ptag]:
					transition[ptag][ntag] = math.log(ld * float(transition_num[ptag][ntag])/sum(transition_num[ptag].values()) + (1-ld)*float(tag_counts[ntag])/ notags)
				else:
					transition[ptag][ntag] =  math.log(float((1-ld)*float(tag_counts[ntag])/ notags))
			else:
				transition[ptag][ntag] =  math.log(float((1-ld)*float(tag_counts[ntag])/ notags))
		# print tag_counts[ntag] 
		# print notags
		tps[ntag] = math.log(float(tag_counts[ntag])/notags)
		for k in word_counts:
				if k not in emission:
					emission[k] ={}
				if  k in emission_num:
					if ntag in emission_num[k]:
						emission[k][ntag] = math.log(wd* float(emission_num[k][ntag])/(tag_counts[ntag]) +  (1-wd)*float(word_counts[k])/ nowords)
						# if emission_num[k][ntag] ==1:
						# 	if ntag in unknown:
						# 		unknown[ntag] +=1 
						# 	else :
						# 		unknown[ntag] =1
						# else:
						# 	if ntag not in unknown:
						# 		unknown[ntag] =0
					else :
						emission[k][ntag]= math.log((1-wd)*float(word_counts[k])/ nowords)
				else:
					emission[k][ntag]= math.log((1-wd)*float(word_counts[k])/ nowords)
	tps['q'] = math.log(float(qc)/notags)
	print tps
	# 	if unknown[ntag]>0:
	# 		unknown[ntag] = math.log(float(unknown[ntag])/tag_counts[ntag])
	# 	else:
	# 		unknown[ntag] =0
	# print unknown
	# for k in emission_num :
	# 	for tag in emission_num[k]:
	# 		if k not in emission:
	# 			emission[k]={}
	# 		emission[k][tag] = math.log(float(emission_num[k][tag])/tag_counts[tag])
	# print transition['q']
	# print len(transition_num['q'])
	# print len(transition['q'])
	# print emission['from']
	# print("--- %s seconds ---" % (time.time() - start_time))
	# print emission
	# print transition
	# print ("emission",emission['from'])
	# print ("transistion",transition['q'])
	# print emission['ap']
	print  max(tag_counts,key=lambda item:tag_counts[item])
	# print tag_counts['VERB']
	hmmmodel = [transition,emission,tc,tps]
	with open('hmmmodel.txt', 'wb') as handle:
		pickle.dump(hmmmodel, handle, protocol=0)


if __name__ == "__main__":
    start_time = time.time()
    arg1 = sys.argv[1]
    readTrain(arg1)
    print("--- %s seconds ---" % (time.time() - start_time))