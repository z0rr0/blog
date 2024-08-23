package example

import "testing"

const (
	stop = 10_000
	step = 2
)

// how to run
// go test -bench=. -benchmem iterators-in-go

func BenchmarkChanIterator(b *testing.B) {
	for i := 0; i < b.N; i++ {
		j := i
		c := ChanIterator(i, i+stop, step)

		for k := range c {
			if k != j {
				b.Errorf("failed %v != %v", k, j)
			}
			j += step
		}
	}
}

func BenchmarkFuncIterator(b *testing.B) {
	for i := 0; i < b.N; i++ {
		j := i
		funcIterator := FuncIterator(i, i+stop, step)

		for k, err := funcIterator(); err == nil; k, err = funcIterator() {
			if k != j {
				b.Errorf("failed %v != %v", k, j)
			}
			j += step
		}
	}
}

func BenchmarkStructIterator(b *testing.B) {
	for i := 0; i < b.N; i++ {
		j := i
		structIterator := &StructIterator{current: i, stop: i + stop, step: step}

		for k, ok := structIterator.Next(); ok; k, ok = structIterator.Next() {
			if k != j {
				b.Errorf("failed %v != %v", k, j)
			}
			j += step
		}
	}
}

func BenchmarkNativeIterator(b *testing.B) {
	for i := 0; i < b.N; i++ {
		j := i
		nativeIterator := NativeIterator(i, i+stop, step)

		for k := range nativeIterator {
			if k != j {
				b.Errorf("failed %v != %v", k, j)
			}
			j += step
		}
	}
}
