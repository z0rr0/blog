# Generators in Go

> **Disclaimer**
> 
> It is not an example for production code.
> 
> It is bad practice to move patterns from known programming language to new one. But sometimes you can adapt them.

---

Many programming languages have a special type of collection called *generator*. It’s lazy structure, that works with one item in one time. So it is more efficiency by memory but you can iterate by objects only once.

*Python example*
```python
def gen(start: int, stop: int, step: int) -> Generator[int, None, None]:
    x = start
    while x < stop:
        yield x
        x += step

g = gen(5, 20, 3)
print(g)
# <generator object gen at 0x104c85f20>

print(list(g))
# [5, 8, 11, 14, 17]

# second call returns empty list
print(list(g))
# []
```

Go language doesn't have generators in the standard library. Let’s write three different implementation of this pattern and compare them.

###  Channel generator

Go channel is a nice mechanism for concurrency communication. One goroutine writes (generate) data to channel and another reads this value. Every time we work only with one item.

```go
import "fmt"

// ErrOffsetIteration is error for failed step/size value.
var ErrOffsetIteration = errors.New("iteration offset must be positive")

// ChanGenerator is a range generator.
func ChanGenerator(start, stop, step int) (chan int, error) {
	if step < 1 {
		return nil, ErrOffsetIteration
	}
	c := make(chan int)
	go func() {
		for j := start; j < stop; j += step {
			c <- j
		}
		close(c)
	}()
	return c, nil
}

// how to use it (without error check)
g, _ := ChanGenerator(5, 20, 3)
for j := range g {
    fmt.Println(j)
}
```

Many consumers can safety read generator’s data from channel, but it should be slowly due to internal locks, we will check this later.

### Function generator

The second implementation is a function with closure. We create initial state `i` and modify it inside an internal returned anonymous function.

```go
import (
    "sync"
    "fmt"
)

// ErrStopIteration is error when iteration is finished.
var ErrStopIteration = errors.New("stop iteration")

// FuncGenerator is a function closure int generator.
func FuncGenerator(start, stop, step int) func() (int, error) {
	if step < 1 {
		return func() (int, error) {
            return 0, ErrOffsetIteration
        }
	}
	var m sync.Mutex
	i := start
	return func() (int, error) {
		m.Lock()
		defer func() {
			i += step
			m.Unlock()
		}()
		if i >= stop {
			step = 0
			return 0, ErrStopIteration
		}
		return i, nil
	}
}

// how to use it
var (
	j   int
	err error
)
g := FuncGenerator(5, 20, 3)
for j, err = g(); err == nil; j, err = g() {
	fmt.Println(j)
}
if err != ErrStopIteration {
	fmt.Println("oops")
	// handle error
}
```

Mutex is required here, because concurrent function calls can update `i` in parallel.

```
goos: darwin
goarch: amd64
pkg: github.com/z0rr0/blog/posts/go-generators/example
cpu: Intel(R) Core(TM) i5-1038NG7 CPU @ 2.00GHz
BenchmarkChanGenerator-8               5596 204634 ns/op  145 B/op  2 allocs/op
BenchmarkChanChunk-8                  10000 107430 ns/op  161 B/op  2 allocs/op
BenchmarkFuncGenerator-8              66406  17380 ns/op   72 B/op  4 allocs/op
BenchmarkChunkGenerator-8            114096  10245 ns/op   88 B/op  4 allocs/op
BenchmarkStructGenerator_Next-8       65679  17409 ns/op   64 B/op  1 allocs/op
BenchmarkStructGenerator_NextChunk-8 126115   9233 ns/op   64 B/op  1 allocs/op
```