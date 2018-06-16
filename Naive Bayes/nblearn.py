import sys
import cPickle as pickle
import math
import time
import string

classes = {}
classes['Pos']=0
classes['Neg']=0
classes['True']=0
classes['Fake']=0
bow={}
bow['Pos'] ={}
bow['Neg'] ={}
bow['Fake'] ={}
bow['True'] ={}
probs ={}
vocab ={}
vocab['Pos'] =0
vocab['Neg'] =0
vocab['Fake'] =0
vocab['True'] =0
trained={}
trained['Pos'] ={}
trained['Neg'] ={}
trained['Fake'] ={}
trained['True'] ={}
pclass = {}
pclass['Pos']=0
pclass['Neg']=0
pclass['True']=0
pclass['Fake']=0
tfidf={}
tfidf['Pos'] ={}
tfidf['Neg'] ={}
tfidf['Fake'] ={}
tfidf['True'] ={}
sumtfidf ={}
sumtfidf['Pos'] =0
sumtfidf['Neg'] =0
sumtfidf['Fake'] =0
sumtfidf['True'] =0
tmodified =0


def bag_of_words(ftrain):	
	with open('nbmodel.txt', 'wb') as handle:
		file = open(ftrain,"r")
		text = file.readlines()
		for line in text:
			line = line.split(' ')
			c1 = line[1]
			classes[c1] = classes[c1] +1
			c2 = line[2]
			classes[c2] =classes[c2] +1
			#print ' '.join(line[3:])
			s= ' '.join(line[3:]).lower().replace('"','').replace('(','').replace(')','').replace('\n','').replace(',','').replace('.','').replace('!','')
			# s = s.translate(None, string.punctuation)
			txt = s.split(' ')
			vocab[c1] = vocab[c1] + len(set(txt))
			vocab[c2] = vocab[c2] + len(set(txt))
			words_added = []
			for word in txt :
				if word not in probs:
					probs[word] = 1
				else:
					probs[word] +=1
				if word in words_added :
					continue
				words_added.append(word)
				if word in bow[c1] :
					bow[c1][word.lower()] = bow[c1][word.lower()] +1
				else:
					bow[c1][word.lower()] =1
				if word in bow[c2] :
					bow[c2][word.lower()] = bow[c2][word.lower()] +1
				else:
					bow[c2][word.lower()] =1
		alpha = 0.9999
		for word in probs:
			for c in classes:
				if word in bow[c] :
					trained[c][word] = math.log(float(alpha * bow[c][word])/(vocab[c]) + float((1-alpha)*classes[c])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
				else:
					trained[c][word] = math.log(float((1-alpha)*classes[c])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		# print trained, len(trained)
		pclass['Pos']=math.log(float(classes['Pos'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		pclass['Neg']=math.log(float(classes['Neg'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		pclass['True']=math.log(float(classes['True'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		pclass['Fake']=math.log(float(classes['Fake'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		words = sorted(probs, key=probs.get)[-10:]
		print words
		model = [trained,pclass,words]
		pickle.dump(model, handle, protocol=0)


def tf_idf(ftrain):
	with open('nbmodel.txt', 'wb') as handle:
		file = open(ftrain,"r")
		count =0
		text = file.readlines()
		for line in text:
			count =count+1
			line = line.split(' ')
			c1 = line[1]
			classes[c1] = classes[c1] +1
			c2 = line[2]
			classes[c2] =classes[c2] +1
			txt = line[3].lower().replace('\n','').split(' ')
			vocab[c1] = vocab[c1] + len(txt)
			vocab[c2] = vocab[c2] + len(txt)
			for word in txt :
				if word not in probs:
					probs[word] = 1
					break
				else:
					probs[word] +=1
					break
				# if word in bow[c1] :
				# 	bow[c1][word.lower()] = bow[c1][word.lower()] +1
				# else:
				# 	bow[c1][word.lower()] =1
				# if word in bow[c2] :
				# 	bow[c2][word.lower()] = bow[c2][word.lower()] +1
				# else:
				# 	bow[c2][word.lower()] =1
		# for key in bow:
		# 	for word in bow[key] :
		# 		tfidf[key][word] = bow[key][word] * math.log(float(4)/probs[word])
		# 		sumtfidf[key] += tfidf[key][word]
		# #print sumtfidf
		#print trained, len(trained)
		for line in text:
			line = line.split(' ')
			c1 = line[1]
			c2 = line[2]
			txt = line[3].lower().replace('\n','').split(' ')
			for word in probs:
				tfidf = txt.count(word) * math.log(float(count)/probs[word])
				sumtfidf[c1] += tfidf
				sumtfidf[c2] += tfidf
				if word in bow[c1] :
					bow[c1][word.lower()] = bow[c1][word.lower()] + tfidf
				else:
					bow[c1][word.lower()] = tfidf
				if word in bow[c2] :
					bow[c2][word.lower()] = bow[c2][word.lower()] + tfidf
				else:
					bow[c2][word.lower()] = tfidf
		print bow
		for word in probs:
			for c in classes:
				if word in bow[c] :
					trained[c][word] = math.log(float(bow[c][word] +1)/(sumtfidf[c]+len(probs)))
				else:
					trained[c][word] = math.log(float(1)/(sumtfidf[c]+len(probs)))


		pclass['Pos']=math.log(float(classes['Pos'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		pclass['Neg']=math.log(float(classes['Neg'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		pclass['True']=math.log(float(classes['True'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		pclass['Fake']=math.log(float(classes['Fake'])/(classes['Pos']+classes['Neg']+classes['True']+classes['Fake']))
		model = [trained,pclass]
		pickle.dump(model, handle, protocol=0)

if __name__ == "__main__":
    start_time = time.time()
    arg1 = sys.argv[1]
    bag_of_words(arg1)
    print("--- %s seconds ---" % (time.time() - start_time))








