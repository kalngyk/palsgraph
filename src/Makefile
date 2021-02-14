all: palsgetpos.so

palsgetpos.so:
	c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` palsgetpos.cpp -o $@

clean:
	rm -f *.o *.so
