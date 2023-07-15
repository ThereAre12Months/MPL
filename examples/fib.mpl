let a 0;
let b 1;

out(a);

let count 0;

repeat 4 {
    a <-> b;
    b += a;
    out(a);
    count += 1;
};