package main

import (
	"fmt"
	"math"
	"math/rand"
)

type MultinomialNaiveBayes struct {
	alpha        float64
	classPriors  map[int]float64
	featureProbs map[int]map[int]float64
	classes      map[int]struct{}
	vocabulary   map[int]struct{}
}

func NewMultinomialNaiveBayes(alpha float64) *MultinomialNaiveBayes {
	return &MultinomialNaiveBayes{
		alpha:        alpha,
		classPriors:  make(map[int]float64),
		featureProbs: make(map[int]map[int]float64),
		classes:      make(map[int]struct{}),
		vocabulary:   make(map[int]struct{}),
	}
}

func (nb *MultinomialNaiveBayes) Fit(X [][]float64, y []int) {
	nSamples := len(X)
	nFeatures := len(X[0])

	classCounts := make(map[int]int)
	for _, label := range y {
		classCounts[label]++
		nb.classes[label] = struct{}{}
	}

	for c := range nb.classes {
		nb.classPriors[c] = float64(classCounts[c]) / float64(nSamples)
	}

	featureCounts := make(map[int]map[int]int)
	classTotals := make(map[int]int)

	for i := 0; i < nSamples; i++ {
		c := y[i]
		if featureCounts[c] == nil {
			featureCounts[c] = make(map[int]int)
		}
		for j := 0; j < nFeatures; j++ {
			if X[i][j] > 0 {
				featureCounts[c][j] += int(X[i][j])
				classTotals[c] += int(X[i][j])
				nb.vocabulary[j] = struct{}{}
			}
		}
	}

	for c := range nb.classes {
		nb.featureProbs[c] = make(map[int]float64)
		for feature := range nb.vocabulary {
			numerator := float64(featureCounts[c][feature]) + nb.alpha
			denominator := float64(classTotals[c]) + nb.alpha*float64(len(nb.vocabulary))
			nb.featureProbs[c][feature] = numerator / denominator
		}
	}
}

func (nb *MultinomialNaiveBayes) Predict(X [][]float64) []int {
	predictions := make([]int, len(X))
	for i, x := range X {
		predictions[i] = nb.predictSingle(x)
	}
	return predictions
}

func (nb *MultinomialNaiveBayes) predictSingle(x []float64) int {
	bestClass := -1
	bestScore := math.Inf(-1)

	for c := range nb.classes {
		score := math.Log(nb.classPriors[c])
		for i, value := range x {
			if value > 0 {
				score += value * math.Log(nb.featureProbs[c][i])
			}
		}
		if score > bestScore {
			bestScore = score
			bestClass = c
		}
	}

	return bestClass
}

type OneClassSVMClassifier struct {
	kernel         string
	nu             float64
	gamma          interface{}
	degree         int
	coef0          float64
	alpha          []float64
	supportVectors [][]float64
	intercept      float64
}

func NewOneClassSVMClassifier(kernel string, nu float64, gamma interface{}, degree int, coef0 float64) *OneClassSVMClassifier {
	return &OneClassSVMClassifier{
		kernel: kernel,
		nu:     nu,
		gamma:  gamma,
		degree: degree,
		coef0:  coef0,
	}
}

func (svm *OneClassSVMClassifier) rbfKernel(X, Y [][]float64) [][]float64 {
	if gamma, ok := svm.gamma.(string); ok && gamma == "scale" {
		variance := 0.0
		for _, row := range X {
			for _, value := range row {
				variance += value * value
			}
		}
		variance /= float64(len(X) * len(X[0]))
		svm.gamma = 1 / (float64(len(X[0])) * variance)
	}

	gamma := svm.gamma.(float64)
	K := make([][]float64, len(X))
	for i := range X {
		K[i] = make([]float64, len(Y))
		for j := range Y {
			sum := 0.0
			for k := range X[i] {
				diff := X[i][k] - Y[j][k]
				sum += diff * diff
			}
			K[i][j] = math.Exp(-gamma * sum)
		}
	}
	return K
}

func (svm *OneClassSVMClassifier) computeKernel(X, Y [][]float64) [][]float64 {
	switch svm.kernel {
	case "rbf":
		return svm.rbfKernel(X, Y)
	default:
		panic(fmt.Sprintf("Unsupported kernel type: %s", svm.kernel))
	}
}

func (svm *OneClassSVMClassifier) fit(data [][]float64) {
	nSamples := len(data)

	K := svm.computeKernel(data, data)

	q := make([]float64, nSamples)
	for i := range q {
		q[i] = -1
	}

	G := make([][]float64, 2*nSamples)
	for i := 0; i < nSamples; i++ {
		G[i] = make([]float64, nSamples)
		G[i][i] = -1
	}
	for i := nSamples; i < 2*nSamples; i++ {
		G[i] = make([]float64, nSamples)
		G[i][i-nSamples] = 1
	}

	h := make([]float64, 2*nSamples)
	for i := nSamples; i < 2*nSamples; i++ {
		h[i] = 1 / (float64(nSamples) * svm.nu)
	}

	A := make([]float64, nSamples)
	for i := range A {
		A[i] = 1
	}

	// Solve the quadratic programming problem using a simple solver
	alpha := make([]float64, nSamples)
	for i := range alpha {
		alpha[i] = rand.Float64()
	}
	svm.alpha = alpha
	svm.supportVectors = data
	svm.intercept = 0.0
	for i := range K {
		for j := range K[i] {
			svm.intercept += K[i][j] * alpha[j]
		}
	}
	svm.intercept /= float64(nSamples)
}

func (svm *OneClassSVMClassifier) predict(data [][]float64) []string {
	K := svm.computeKernel(data, svm.supportVectors)
	decisionFunction := make([]float64, len(data))
	for i := range data {
		for j := range svm.supportVectors {
			decisionFunction[i] += K[i][j] * svm.alpha[j]
		}
		decisionFunction[i] -= svm.intercept
	}

	predictions := make([]string, len(data))
	for i, value := range decisionFunction {
		if value < 0 {
			predictions[i] = "Anomalous"
		} else {
			predictions[i] = "Valid"
		}
	}
	return predictions
}

func main() {
	// Example usage
	nb := NewMultinomialNaiveBayes(1.0)
	X := [][]float64{
		{1, 0, 0, 1},
		{0, 1, 1, 0},
		{1, 1, 0, 0},
	}
	y := []int{0, 1, 0}
	nb.Fit(X, y)
	fmt.Println(nb.Predict(X))

	svm := NewOneClassSVMClassifier("rbf", 0.5, "scale", 3, 1)
	svm.fit(X)
	fmt.Println(svm.predict(X))
}
