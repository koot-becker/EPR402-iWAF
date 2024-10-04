package main

import (
	"fmt"
	"regexp"
	"strings"
)

type SimpleCountVectorizer struct {
	vocabulary map[string]int
	vocabSize  int
}

func NewSimpleCountVectorizer() *SimpleCountVectorizer {
	return &SimpleCountVectorizer{
		vocabulary: make(map[string]int),
		vocabSize:  0,
	}
}

func (scv *SimpleCountVectorizer) Fit(texts []string) {
	wordCount := make(map[string]int)
	for _, text := range texts {
		words := scv.tokenize(text)
		for _, word := range words {
			wordCount[word]++
		}
	}

	idx := 0
	for word := range wordCount {
		scv.vocabulary[word] = idx
		idx++
	}
	scv.vocabSize = len(scv.vocabulary)
}

func (scv *SimpleCountVectorizer) Transform(texts []string) *mat.Dense {
	rows := len(texts)
	cols := scv.vocabSize
	data := make([]float64, rows*cols)

	for row, text := range texts {
		wordCounts := make(map[string]int)
		words := scv.tokenize(text)
		for _, word := range words {
			wordCounts[word]++
		}
		for word, count := range wordCounts {
			if col, ok := scv.vocabulary[word]; ok {
				data[row*cols+col] = float64(count)
			}
		}
	}

	return mat.NewDense(rows, cols, data)
}

func (scv *SimpleCountVectorizer) FitTransform(texts []string) *mat.Dense {
	scv.fit(texts)
	return scv.transform(texts)
}

func (scv *SimpleCountVectorizer) tokenize(text string) []string {
	re := regexp.MustCompile(`\b\w+\b`)
	return re.FindAllString(strings.ToLower(text), -1)
}

func main() {
	// Example usage
	texts := []string{"This is a test.", "This test is only a test."}
	vectorizer := NewSimpleCountVectorizer()
	vectorizer.Fit(texts)
	matrix := vectorizer.Transform(texts)

	// Print the resulting matrix
	matPrint(matrix)
}

func matPrint(X mat.Matrix) {
	fa := mat.Formatted(X, mat.Prefix(""), mat.Squeeze())
	fmt.Printf("%v\n", fa)
}
