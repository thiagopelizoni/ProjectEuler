// Problem: https://projecteuler.net/problem=140
package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

const targetCount = 30

func findFibonacciGaussianNumbers(start, end int64, results chan int64, wg *sync.WaitGroup) {
    defer wg.Done()
    perfectSquare := int64(1)
    increment := int64(1)
    for x := start; x <= end; x++ {
        testValue := 1 + 14*x + 5*x*x
        for perfectSquare < testValue {
            perfectSquare += (2 * increment) + 1
            increment++
        }
        if testValue == perfectSquare {
            results <- x
        }
    }
}

func main() {
    startTime := time.Now()

    numCPU := runtime.NumCPU()
    runtime.GOMAXPROCS(numCPU) 

    var wg sync.WaitGroup
    results := make(chan int64)

    searchBlockSize := int64(100000000000000) 
    for start := int64(1); start < searchBlockSize*targetCount; start += searchBlockSize {
        end := start + searchBlockSize - 1
        if end > searchBlockSize*targetCount {
            end = searchBlockSize*targetCount - 1
        }
        wg.Add(1)
        go findFibonacciGaussianNumbers(start, end, results, &wg)
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    total := int64(0)
    count := 0
    for fibonacciGaussianNumber := range results {
        fmt.Println(count+1, "\t", fibonacciGaussianNumber)
        total += fibonacciGaussianNumber
        count++
    }
    fmt.Println("==========")
    fmt.Println(total)

    fmt.Println("Elapsed time:", time.Since(startTime))
}