// Problem: https://projecteuler.net/problem=144
package main

import (
	"fmt"
	"math"
	"runtime"
)

func computeLeftSlope(interceptSlope, intercept float64) (x, y float64) {
	x = (-intercept*interceptSlope - 2*math.Sqrt(100-(intercept*intercept)+(25*interceptSlope*interceptSlope))) / (4 + interceptSlope*interceptSlope)
	y = interceptSlope*x + intercept
	return
}

func computeRightSlope(interceptSlope, intercept float64) (x, y float64) {
	x = (-intercept*interceptSlope + 2*math.Sqrt(100-(intercept*intercept)+(25*interceptSlope*interceptSlope))) / (4 + interceptSlope*interceptSlope)
	y = interceptSlope*x + intercept
	return
}

func calculateNormal(x, y float64) float64 {
	return y / (4 * x)
}

func calculateReflection(normalSlope, initialSlope float64) float64 {
	return (2*normalSlope - initialSlope*(1-(normalSlope*normalSlope))) / (1 + (2 * initialSlope * normalSlope) - (normalSlope * normalSlope))
}

func calculateIntercept(x, y, slope float64) float64 {
	return (-slope * x) + y
}

func worker(tasks <-chan [3]float64, results chan<- [3]float64) {
	for task := range tasks {
		x, y, initialSlope := task[0], task[1], task[2]
		reflectedSlope := calculateReflection(calculateNormal(x, y), initialSlope)
		newIntercept := calculateIntercept(x, y, reflectedSlope)
		leftX, _ := computeLeftSlope(reflectedSlope, newIntercept)
		rightX, _ := computeRightSlope(reflectedSlope, newIntercept)

		if math.Abs(leftX-x) > math.Abs(rightX-x) {
			x, y = computeLeftSlope(reflectedSlope, newIntercept)
		} else {
			x, y = computeRightSlope(reflectedSlope, newIntercept)
		}
		results <- [3]float64{x, y, reflectedSlope}
	}
}

func main() {
	numCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(numCPU)

	initialSlope := -(197.0 / 14.0)
	intercept := 10.1

	x, y := computeRightSlope(initialSlope, intercept)

	tasks := make(chan [3]float64, numCPU)
	results := make(chan [3]float64, numCPU)

	for i := 0; i < numCPU; i++ {
		go worker(tasks, results)
	}

	count := 0

	for math.Abs(x) > .01 || y < 0 {
		tasks <- [3]float64{x, y, initialSlope}
		result := <-results
		x, y, initialSlope = result[0], result[1], result[2]
		count++
	}

	close(tasks)
	close(results)

	fmt.Println(count)
}
