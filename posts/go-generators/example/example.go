package example

import (
	"errors"
	"sync"
)

var (
	// ErrStopIteration is error when iteration is finished.
	ErrStopIteration = errors.New("stop iteration")
	// ErrOffsetIteration is error for failed step/size value.
	ErrOffsetIteration = errors.New("iteration offset must be positive")
)

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

// ChunkChanGenerator splits items by chunks with maximum length=size.
func ChunkChanGenerator(items []int, size int) (chan []int, error) {
	if size < 1 {
		return nil, ErrOffsetIteration
	}
	c := make(chan []int)
	start, stop := 0, len(items)
	go func() {
		defer close(c)
		for j := start; j < stop; j += size {
			step := j + size
			if step > stop {
				c <- items[j:stop]
				return // last chunk
			}
			c <- items[j:step]
		}
	}()
	return c, nil
}

// FuncGenerator is a function closure int generator.
func FuncGenerator(start, stop, step int) func() (int, error) {
	if step < 1 {
		return func() (int, error) { return 0, ErrOffsetIteration }
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

// ChunkFuncGenerator is a function closure chunk splitter.
func ChunkFuncGenerator(items []int, size int) func() ([]int, error) {
	if size < 1 {
		return func() ([]int, error) { return nil, ErrOffsetIteration }
	}
	var m sync.Mutex
	j, stop := 0, len(items)
	return func() ([]int, error) {
		m.Lock()
		defer func() {
			j += size
			m.Unlock()
		}()
		if j >= stop {
			size = 0
			return nil, ErrStopIteration
		}
		step := j + size
		if step > stop {
			step = stop
		}
		return items[j:step], nil
	}
}

// StructGenerator is a struct generator.
type StructGenerator struct {
	sync.Mutex
	stop  int
	step  int
	value int
	items []int
}

// NewStructGenerator returns a new struct generator.
func NewStructGenerator(start, stop, step int) (*StructGenerator, error) {
	if step < 1 {
		return nil, ErrOffsetIteration
	}
	return &StructGenerator{stop: stop, step: step, value: start}, nil
}

// NewGenStructChunk returns new chunk splitter.
func NewGenStructChunk(items []int, size int) (*StructGenerator, error) {
	if size < 1 {
		return nil, ErrOffsetIteration
	}
	return &StructGenerator{stop: len(items), step: size, items: items}, nil
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

// NextChunk returns a new generated chunk and flag that it is not the end.
func (g *StructGenerator) NextChunk() ([]int, bool) {
	g.Lock()
	i := g.value + g.step
	if i > g.stop {
		i = g.stop
	}
	defer func() {
		g.value = i
		g.Unlock()
	}()
	return g.items[g.value:i], g.value < g.stop
}
