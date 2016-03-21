#!/usr/bin/env python
from FeedforwardSingleNeuralNetwork import FeedforwardSingleNeuralNetwork
import numpy as np

class Main:

	def findMaxNumberOfApps(self, file):
		file.seek(0)
		apps = []

		for line in file:
			tuples = line.split(';')
		
			for t in range(len(tuples)):
				tup = tuples[t]
				vals = tup.split(',')
				apps.append(vals[0])
		
		return max(apps)
	
	# 1. Battery Level => 0-6
	# 2. Brightness Level => 0-4
	# 3. Screen Orientarion => 0-2
	# 4. Power => 0-2
	# 5. Headset => 0-2
	# 6. App => 0-X
	# 7. Last Period of the Day => 0-4
	# 8. Last Time between apps => 0-5
	# 9. Las GPS => 0-3
	def createNeuronInput(self, activatedValue, maxValue):
		
		inputs = []

		for pos in range(int(maxValue) + 1):
			if(pos != int(activatedValue)):
				inputs.append(0)
			else:
				inputs.append(1)
		
		return inputs



	def run(self):

		rawDataset = open('../selectedUserMore', 'r')

		# Value 0 represents max number of apps => It must be set
		maxValuesByFeature = [6,4,2,2,2,0,4,5,3]

		datasetFeatures = []
		datasetLabels = []

		maxApps = self.findMaxNumberOfApps(rawDataset)

		# Setting max number of apps
		maxValuesByFeature[5] = maxApps

		rawDataset.seek(0)
		for line in rawDataset:
			tuples = line.split(';')

			for t in range(len(tuples)):

				
				listFeatureNeurons = []
				listLabelNeurons = []

				tup = tuples[t]
				vals = tup.split(',')
				label = vals[0]
				features = vals[1].split('_')
				
				for feature in range(len(features)):
					val = features[feature]
					listFeatureNeurons += self.createNeuronInput(val, maxValuesByFeature[feature])
				
				listLabelNeurons += self.createNeuronInput(label, maxApps)

				datasetFeatures.append(listFeatureNeurons)
				datasetLabels.append(listLabelNeurons)

		rawDataset.close()		

		nTuples = len(datasetLabels)

		nTrain = int(0.7 * nTuples)

		trainSetFeatures = datasetFeatures[:nTrain]
		trainSetLabels = datasetLabels[:nTrain]

		testSetFeatures = datasetFeatures[nTrain:]
		testSetLabels = datasetLabels[nTrain:]



		ffsn = FeedforwardSingleNeuralNetwork(10)
		ffsn.train(trainSetFeatures, trainSetLabels)
		
		results = ffsn.predict(testSetFeatures)

		nPredictedCorrectly = 0	

		for test in range(len(testSetLabels)):
			realValue = testSetLabels[test].index(1)
			predictedValue = np.argmax(results[test])	
			
			if(int(realValue) == int(predictedValue)):
				++nPredictedCorrectly

				
			# print "Real: " + str(realValue) + " / Predicted: " + str(predictedValue)	

		print nPredictedCorrectly	
		print "Accuracy: " + str(float(nPredictedCorrectly / (nTuples - nTrain)))	

main = Main()
main.run()


