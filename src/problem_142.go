// Problem: https://projecteuler.net/problem=142
package main

import (
    "fmt"
    "math"
    "runtime"
    "sync"
    "time"
)

const maxHypotenuseSquared = 5000
const numCalculations = 200000

func isPerfectSquare(n int64) bool {
    sqrt := int64(math.Sqrt(float64(n)))
    return sqrt*sqrt == n
}

func findMinimumPerimeter(triplesByHypotenuseSquared map[int64]map[int64]bool, minPerimeter *int64, minPerimeterMutex *sync.Mutex, startIndex, chunkSize int64, wg *sync.WaitGroup) {
    defer wg.Done()
    for x := startIndex; x < startIndex+chunkSize; x++ {
        if x%(numCalculations/20) == 0 {
            fmt.Println("x =", x)
        }
        for hypotenuseSquared, baseSquares := range triplesByHypotenuseSquared {
            z := x + hypotenuseSquared
            if x+x+z < *minPerimeter && isPerfectSquare(x+z) {
                for baseSquared := range baseSquares {
                    y := x + baseSquared
                    if x+y+z < *minPerimeter && isPerfectSquare(x+y) && isPerfectSquare(z+y) {
                        minPerimeterMutex.Lock()
                        if x+y+z < *minPerimeter {
                            *minPerimeter = x + y + z
                            fmt.Println(x, "+", y, "+", z, "=", *minPerimeter)
                        }
                        minPerimeterMutex.Unlock()
                    }
                }
            }
        }
    }
}

func main() {
    startTime := time.Now()

    triplesByHypotenuseSquared := make(map[int64]map[int64]bool)
    for base := int64(1); base < maxHypotenuseSquared; base++ {
        for perpendicular := base; perpendicular < maxHypotenuseSquared; perpendicular++ {
            hypotenuseSquared := base*base + perpendicular*perpendicular
            if isPerfectSquare(hypotenuseSquared) {
                if _, exists := triplesByHypotenuseSquared[hypotenuseSquared]; exists {
                    triplesByHypotenuseSquared[hypotenuseSquared][base*base] = true
                    triplesByHypotenuseSquared[hypotenuseSquared][perpendicular*perpendicular] = true
                } else {
                    triplesByHypotenuseSquared[hypotenuseSquared] = make(map[int64]bool)
                    triplesByHypotenuseSquared[hypotenuseSquared][base*base] = true
                    triplesByHypotenuseSquared[hypotenuseSquared][perpendicular*perpendicular] = true
                }
            }
        }
    }
    fmt.Println("Tabela de triplas pitagóricas construída em", time.Since(startTime))

    minPerimeter := int64(3*numCalculations + 3*maxHypotenuseSquared*maxHypotenuseSquared)
    var minPerimeterMutex sync.Mutex
    
    var wg sync.WaitGroup

    numCPU := runtime.NumCPU()
    runtime.GOMAXPROCS(numCPU)

    chunkSize := int64(numCalculations) / int64(numCPU)
    for i := 0; i < numCPU; i++ {
        wg.Add(1)
        go findMinimumPerimeter(triplesByHypotenuseSquared, &minPerimeter, &minPerimeterMutex, int64(i)*chunkSize, chunkSize, &wg) // Passa &wg para a goroutine
    }
    wg.Wait()

    fmt.Println("Tempo decorrido:", time.Since(startTime))
}
