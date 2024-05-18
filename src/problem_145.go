// Problem: https://projecteuler.net/problem=145
package main

import (
	"fmt"
	"runtime"
	"strconv"
	"sync"
	"time"
)

func containsOnlyOddDigits(number int64) bool {
	numberStr := strconv.FormatInt(number, 10)
	for i := 0; i < len(numberStr); i++ {
		digit, _ := strconv.Atoi(numberStr[i : i+1])
		if digit%2 == 0 {
			return false
		}
	}
	return true
}

func reverseInt(n int64) int64 {
	reversed := int64(0)
	for n > 0 {
		reversed = reversed*10 + n%10
		n /= 10
	}
	return reversed
}

func main() {
	startTime := time.Now()

	numCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(numCPU)

	var wg sync.WaitGroup
	var mutex sync.Mutex

	totalCount := 0
	chunkSize := int64(100000000 / numCPU)

	for i := 0; i < numCPU; i++ {
		wg.Add(1)
		go func(start int64) {
			defer wg.Done()
			localCount := 0
			for j := start; j < start+chunkSize; j++ {
				if containsOnlyOddDigits(j+reverseInt(j)) && j%10 != 0 {
					localCount++
				}
			}
			mutex.Lock()
			totalCount += localCount
			mutex.Unlock()
		}(int64(i) * chunkSize)
	}

	wg.Wait()

	fmt.Println(totalCount)
	fmt.Println("Elapsed time:", time.Since(startTime))
}