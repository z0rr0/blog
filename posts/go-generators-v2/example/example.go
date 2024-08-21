package example

import (
	"errors"
	"iter"
	"sync"
)

// ChanIterator is a range generator using a channel.
func ChanIterator(start, stop, step int) chan int {
	c := make(chan int, 1) // add small to improve performance

	go func() {
		for i := start; i < stop; i += step {
			c <- i
		}
		close(c)
	}()

	return c
}

// ErrStopIteration is an error to indicate the end of the iteration.
var ErrStopIteration = errors.New("stop iteration")

// FuncIterator is a function closure int-value iterator.
func FuncIterator(start, stop, step int) func() (int, error) {
	var (
		m sync.Mutex
		i = start
	)
	return func() (int, error) {
		m.Lock()
		defer func() {
			i += step
			m.Unlock()
		}()

		if i >= stop {
			return 0, ErrStopIteration
		}

		return i, nil
	}
}

// StructIterator is a struct to iterate over a range of integers.
type StructIterator struct {
	sync.Mutex
	current int
	stop    int
	step    int
}

// Next returns a new generation value and flag that it is not the end.
func (g *StructIterator) Next() (int, bool) {
	defer func() {
		g.Lock()
		g.current += g.step
		g.Unlock()
	}()
	return g.current, g.current < g.stop
}


// NativeIterator is a native iterator for go since 1.23
func NativeIterator(start, stop, step int) iter.Seq[int] {
	return func(yield func(int) bool) {
		for i := start; i < stop; i += step {
			if !yield(i) {
				return
			}
		}
	}
}