fn i32 fib(i32 n, i32 unused) {
    if n < 2 {
        return n;
    }
    return fib(n - 1, 0) + fib(n - 2, 0);
}

fn i32 main() {
    if (5 > 10) {
        return 0;
    }
    return fib(10, 0);
}