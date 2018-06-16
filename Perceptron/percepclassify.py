import sys
import cPickle as pickle
import time
import string
import operator
import copy

def get_features(fpredict,fmodel):
	global model
	examples = []
	i=0
	lid =[]
	with open(fmodel, 'rb') as handle:
		model = pickle.load(handle)
		features = model[4]
		file = open(fpredict,"r")
		lines = file.readlines()
		file.close()
	for line in lines:
			line = line.split(' ')
			lid.append(line[0])
			# s= ' '.join(line[1:]).lower().replace('\n','').replace('"','').replace('(','').replace(')','').replace('\n','').lower().replace(',','').replace('.','').replace('!','')
			s= ' '.join(line[1:]).lower().replace('\n','')
			s = s.translate(None, string.punctuation)
			txt = s.split(' ')
			a =[0]*len(features)
			for word in txt:
				if word in features:
					i = features.index(word)
					# print i
					a[i] =1
			examples.append(copy.deepcopy(a))
	get_labels(examples,model,lid)
		# print node1,node2

def get_bigram_features(fpredict,fmodel):
	global model
	examples = []
	i=0
	lid =[]
	with open(fmodel, 'rb') as handle:
		model = pickle.load(handle)
		features = model[4]
		file = open(fpredict,"r")
		lines = file.readlines()
		file.close()
	for line in lines:
			line = line.split(' ')
			lid.append(line[0])
			# s= ' '.join(line[1:]).lower().replace('\n','').replace('"','').replace('(','').replace(')','').replace('\n','').lower().replace(',','').replace('.','').replace('!','')
			s= ' '.join(line[1:]).lower().replace('\n','')
			s = s.translate(None, string.punctuation)
			txt = s.split(' ')
			a =[0]*len(features)
			for word in range(0,len(txt)-1):
				if txt[word] in features:
					i=features.index(txt[word])
					a[i] = 1
				if (txt[word],txt[word+1]) in features:
					i = features.index((txt[word],txt[word+1]))
					a[i] =1
			if txt[len(txt)-1] in features:
					i=features.index(txt[len(txt)-1])
					a[i] = 1
			examples.append(copy.deepcopy(a))
	# print examples
	get_labels(examples,model,lid)

def get_labels(features,model,lid):
	w1 = model[0]
	w2 = model[1]
	b1 = model[2]
	b2=model[3]
	labels =[]
	for wordi in range(0,len(features)):
			n1 = 1 if sum(map(operator.mul,features[wordi],w1))+b1 > 1 else 0
			n2 = 1 if sum(map(operator.mul,features[wordi],w2))+b2 >1 else 0
			labels.append([n1,n2])
			# print n1,n2,node1[wordi],node2[wordi]
	with open('percepoutput.txt', 'w+') as output:
		for h in range(0,len(labels)) :
			if labels[h][0]==0:
				c1 = "Fake"
			else:
				c1 ="True"
			if labels[h][1]==0:
				c2 = "Neg"
			else:
				c2 ="Pos"

			output.write(lid[h]+' '+c1+' '+c2+'\n')
			
		



if __name__ == "__main__":
    start_time = time.time()
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    get_features(arg2,arg1)
    print("--- %s seconds ---" % (time.time() - start_time))