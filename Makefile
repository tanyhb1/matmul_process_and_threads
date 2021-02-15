PROGS := mm_seq
CFLAGS:= -O3 -Wall -Werror -Wextra
SRCS := $(shell ls mm_*.c | grep 'test' -v)
TARGETS :=  $(basename ${SRCS})
EXEC_TEST_NAMES := $(addprefix test_, $(basename ${SRCS} ))
TESTS := test2 test32 test500
all : $(PROGS)

mm_threadsn : mm_threadsn.c mm_test.c mm_test.h
		${CC} mm_threadsn.c mm_test.c -o mm_threadsn -I . ${CFLAGS} -lpthread
mm_threadsn2: mm_threadsn2.c mm_test.c mm_test.h
		${CC} mm_threadsn2.c mm_test.c -o mm_threadsn2 -I . ${CFLAGS} -lpthread
mm_% : mm_%.c mm_test.c mm_test.h
	${CC} mm_$*.c mm_test.c -o $@ -I . ${CFLAGS}

mmf_%: mm_%.c mm_test.c mm_test.h
	${CC} mm_$*.c mm_test.c -o $@ -I . ${CFLAGS} -D name=DDOUBLE_MM

test_mm_%: mm_% test2.txt test32.txt test500.txt
	./mm_$* test2.txt > test2.log
	./mm_$* test32.txt > test32.log
	./mm_$* test500.txt > test500.log


test : ${EXEC_TEST_NAMES}
	
clean :
	rm -f ${TARGETS} *~


