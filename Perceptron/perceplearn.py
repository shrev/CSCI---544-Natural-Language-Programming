import sys
import cPickle as pickle
import time
import string
import operator
import copy
from collections import OrderedDict
from random import shuffle



word_counts={}
bigram_counts = {}
features =[]
classes=[]
weights = [0]*1000
stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']


def get_features(ftrain):
	global word_counts
	file = open(ftrain,"r")
	text = file.readlines()
	for line in text:
		line = line.split(' ')
		c1 = line[1]
		if c1 not in classes:
			classes.append(c1)
		c2 = line[2]
		if c2 not in classes:
			classes.append(c2)
		#print ' '.join(line[3:])
		s= ' '.join(line[3:]).lower().replace('\n','')
		s = s.translate(None, string.punctuation)
		txt = s.split(' ')
		for word in txt:
			# if word in stop_words:
			# 	continue
			if word not in word_counts:
				word_counts[word] = 1
			else:
				word_counts[word] +=1
	word_counts = OrderedDict(sorted(word_counts.items(), key=operator.itemgetter(1),reverse=True))
	# features = word_counts.keys()[len(word_counts)/2 -500 if  len(word_counts)/2 -500 >0 else 0 : len(word_counts)/2+500 if len(word_counts)/2+500< len(word_counts) else len(word_counts)-1]
	# print len(features)
	features = word_counts.keys()[15:1015]
	examples = []
	node1 = []
	node2 = []
	for line in text:
		line = line.split(' ')
		c1 = line[1]
		# print c1
		c2  = line[2]
		if c2 == 'Pos':
			node2.append(1)
		else:
			node2.append(0)
		if c1 == 'True':
			node1.append(1)
		else:
			node1.append(0)
		s= ' '.join(line[3:]).lower().replace('\n','')
		s = s.translate(None, string.punctuation)
		txt = s.split(' ')
		a =[0]*len(features)
		for word in txt:
			if word in features:
				i = features.index(word)
				# print i
				a[i] =1
		examples.append(copy.deepcopy(a))
	# print node1,node2
	train_vanilla_network(features,examples,node1,node2)
	train_averaged_network(features,examples,node1,node2)


def get_bigram_features(ftrain):
	global word_counts
	global bigram_counts
	file = open(ftrain,"r")
	text = file.readlines()
	for line in text:
		line = line.split(' ')
		c1 = line[1]
		if c1 not in classes:
			classes.append(c1)
		c2 = line[2]
		if c2 not in classes:
			classes.append(c2)
		#print ' '.join(line[3:])
		s= ' '.join(line[3:]).lower().replace('\n','')
		s = s.translate(None, string.punctuation)
		txt = s.split(' ')
		for word in range(0,len(txt)-1):
			if txt[word] in stop_words or txt[word+1]:
				continue
			if (txt[word],txt[word+1]) not in bigram_counts:
				bigram_counts[(txt[word],txt[word+1])] =1
			else:
				bigram_counts[(txt[word],txt[word+1])] +=1
			if txt[word] not in word_counts:
				word_counts[txt[word]] = 1
			else:
				word_counts[txt[word]] +=1
		if txt[len(txt)-1] not in word_counts:
			word_counts[txt[len(txt)-1]] = 1
		else:
			word_counts[txt[len(txt)-1]] += 1
	word_counts = OrderedDict(sorted(word_counts.items(), key=operator.itemgetter(1),reverse=True))
	bigram_counts = OrderedDict(sorted(bigram_counts.items(), key=operator.itemgetter(1),reverse=True))
	# features = word_counts.keys()[len(word_counts)/2 -500 if  len(word_counts)/2 -500 >0 else 0 : len(word_counts)/2+500 if len(word_counts)/2+500< len(word_counts) else len(word_counts)-1]
	# print len(features)
	features = word_counts.keys()[15:1015]
	bfeatures = bigram_counts.keys()[0:2500]
	examples = []
	bexamples =[]
	node1 = []
	node2 = []
	for line in text:
		line = line.split(' ')
		print line
		c1 = line[1].replace(' ','')
		# print c1
		c2  = line[2].replace(' ','')
		if c2 == 'Pos':
			print "here"
			node2.append(1)
		else:
			node2.append(0)
		if c1 == 'True':
			node1.append(1)
		else:
			node1.append(0)
		s= ' '.join(line[3:]).lower().replace('\n','')
		s = s.translate(None, string.punctuation)
		txt = s.split(' ')
		a =[0]*len(features)
		b = [0]*len(bfeatures)
		for word in range(0,len(txt)-1):
			if txt[word] in features:
				i = features.index(txt[word])
				a[i] =1
			if (txt[word],txt[word+1]) in bfeatures:
				g = bfeatures.index((txt[word],txt[word+1]))
				b[g]=1
		if txt[len(txt)-1] in features:
			i = features.index(txt[len(txt)-1])
			a[i] =1
		bexamples.append(copy.deepcopy(a)+copy.deepcopy(b))		
		# examples.append()
	# print node1,node2
	print "len",len(bfeatures)
	print "flen",len(features)
	train_vanilla_network(features+bfeatures,bexamples,node1,node2)
	train_averaged_network(features+bfeatures,bexamples,node1,node2)
9
def train_vanilla_network(f,features,node1,node2):
	w1 = [0]* len(features[0])
	w2 = [0]*len(features[0])
	# print len(features)

	b1 = 0
	b2 = 0
	count =0
	for i in range(0,100):
		diff=0
		count = count+1
		# c = zip(features,node1,node2)
		# shuffle(c)
		# features,node1,node2 = zip(*c)
		# c=list(zip(features,node1,node2))
		# features,node1,node2 = zip(*c)
		for wordi in range(0,len(features)):
			n1 = 1 if sum(map(operator.mul,features[wordi],w1))+b1 > 1 else 0
			n2 = 1 if sum(map(operator.mul,features[wordi],w2))+b2 >1 else 0
			w1 = map(operator.add,w1,map(operator.mul,[node1[wordi]-n1]*len(features[0]),features[wordi]))
			w2 = map(operator.add,w2,map(operator.mul,[node2[wordi]-n2]*len(features[0]),features[wordi]))
			b2 = b2+(node2[wordi]-n2)
			b1 = b1 +(node1[wordi]-n1)
			# print n1,n2,node1[wordi],node2[wordi]
			diff+=(node1[wordi]-n1)+(node2[wordi]-n2)
			# print len(w1)
			# if count==2:
			# 	break
		if diff==0:
			print count
			break
	model = [w1,w2,b1,b2,f]
	with open('vanillamodel.txt', 'wb') as handle:
		pickle.dump(model, handle, protocol=0)
		
def train_averaged_network(f,features,node1,node2):
	w1 = [0]* len(features[0])
	w2 = [0]*len(features[0])
	u1 = [0]*len(features[0])
	u2 = [0]*len(features[0])
	beta1 = 0
	beta2 =0
	b1 = 0
	b2 = 0
	count =0
	for i in range(0,100):
		diff=0
		for wordi in range(0,len(features)):
			n1 = 1 if sum(map(operator.mul,features[wordi],w1))+b1 > 1 else 0
			n2 = 1 if sum(map(operator.mul,features[wordi],w2))+b2 >1 else 0

			w1 = map(operator.add,w1,map(operator.mul,[node1[wordi]-n1]*len(features[0]),features[wordi]))
			w2 = map(operator.add,w2,map(operator.mul,[node2[wordi]-n2]*len(features[0]),features[wordi]))
			u2 = map(operator.add,u2,map(operator.mul,[(node2[wordi]-n2)*count]*len(features[0]),features[wordi]))
			u1 = map(operator.add,u1,map(operator.mul,[(node1[wordi]-n1)*count]*len(features[0]),features[wordi]))
			b2 = b2+(node2[wordi]-n2)
			b1 = b1 +(node1[wordi]-n1)
			beta1 = beta1 + (node1[wordi]-n1)*count
			beat2 =  beta2 +(node2[wordi]-n2)*count
			# print n1,n2,node1[wordi],node2[wordi]
			diff+=(node1[wordi]-n1)+(node2[wordi]-n2)
			count = count+1
			# print len(w1)
			# if count==2:
			# 	break
		if diff==0:
			print count
			# print map(operator.mul,[float(1)/count]*len(features[0]),u1)
		 	w1 = map(operator.sub,w1,map(operator.mul,[float(1)/count]*len(features[0]),u1)) 
		 	w2 = map(operator.sub,w2,map(operator.mul,[float(1)/count]*len(features[0]),u2))
		 	b1 =  b1 - float(1)/count*beta1
		 	b2 = b2 - float(1)/count*beta2
			break
	model = [w1,w2,b1,b2,f]
	print "featureslen",len(features[0])
	with open('averagedmodel.txt', 'wb') as handle:
		pickle.dump(model, handle, protocol=0)



if __name__ == "__main__":
    start_time = time.time()
    arg1 = sys.argv[1]
    get_bigram_features(arg1)
    print("--- %s seconds ---" % (time.time() - start_time))





