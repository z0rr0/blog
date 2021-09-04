# Generators in Go

> **Disclaimer**
> 
> This is not an example for production code.<br>
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
# because there is no history of returned data
print(list(g))
# []
```

Go language doesn't have generators in the standard library. Let’s write three different implementation of this pattern and compare them.

###  Channel generator

Go channel is a nice mechanism for concurrency communication. One goroutine sends (generate) data to a channel and another receives the value. Every time we work only with one item.

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

Many consumers can safety read generator’s data from a channel, but it should be slowly due to internal locks, we will check this later.

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

Mutex is required here, because concurrent function calls can update `i` in several goroutines.

### Struct generator

The latest generator example is structure. It has a current value and stores additional parameters. Also our structure must have mutex like an example before, because concurrent reading should be safety.

```go
// StructGenerator is a struct generator.
type StructGenerator struct {
	sync.Mutex
	stop  int
	step  int
	value int
}

// NewStructGenerator returns a new struct generator.
func NewStructGenerator(start, stop, step int) (*StructGenerator, error) {
	if step < 1 {
		return nil, ErrOffsetIteration
	}
	return &StructGenerator{stop: stop, step: step, value: start}, nil
}

// Next returns a new generation value and flag that it is not the end.
func (g *StructGenerator) Next() (int, bool) {
	defer func() {
		g.Lock()
		g.value += g.step
		g.Unlock()
	}()
	return g.value, g.value < g.stop
}

// how to use it (without error handling)
g, _ := NewStructGenerator(5, 20, 3)
for v, ok := g.Next(); ok; v, ok = g.Next() {
	fmt.Println(v)
}
```

It’s very easy way, it’s interesting to compare all three methods by speed and memory usage.

## Benchmarks 

I wrote simple [example](https://github.com/z0rr0/blog/blob/main/posts/go-generators/example/example_test.go) using Go benchmark mechanism `testing.B` and  got results:

```
goos: darwin
goarch: amd64
pkg: github.com/z0rr0/blog/posts/go-generators/example
cpu: Intel(R) Core(TM) i5-1038NG7 CPU @ 2.00GHz
BenchmarkChanGenerator-8         5772 205862 ns/op 145 B/op 2 allocs/op
BenchmarkFuncGenerator-8        66204  17777 ns/op  72 B/op 4 allocs/op
BenchmarkStructGenerator_Next-8 65004  18028 ns/op  64 B/op 1 allocs/op
```

The histograms show results more clearly

![time_usage.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1630776197311/GkDOTLWS7.png)

And comparing by memory usage 

![memory_usage.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1630776228708/qTeOSuC3P.png)

## Conclusion

There are different ways to implement generators in Go. Using channels is not the best idea. Of course we need to control  concurrent access, but standard mutex can do it better.

I also wrote examples for chunk generators then we need to split a slice into pieces. For example, we want to convert `[1, 2, 3,… 10]` to 5 chunks by 2 items `[1, 2], [3, 4], … [9, 10]`. The same ways were used for it. You can find it in repo [go-generators/example](https://github.com/z0rr0/blog/tree/main/posts/go-generators/example)