setup(640, 480);
title("Mandelbrot on MPL");

let MAX_ITER 15;

let px 20;
let py 0;

let xz 0;
let yz 0;

let x 0;
let y 0;

let xsq 0;
let ysq 0;

let xt 0;

let iter 0;

let total 0;

let clr color(0);

repeat 640 {
    repeat 480 {
        xz = px;
        xz *= 7;
        xz /= 640;
        xz -= 5;
        xz /= 2;

        yz = py;
        yz /= 240;
        yz -= 1;

        x = 0;
        y = 0;

        iter = 0;
        
        xsq = x;
        xsq *= x;

        ysq = y;
        ysq *= y;

        total = xsq;
        total *= ysq;

        while (total <= 4) {
            xt = xsq;
            xt -= ysq;
            xt += xz;

            y *= 2;
            y *= x;
            y += yz;

            x = xt;

            xsq = x;
            xsq *= x;

            ysq = y;
            ysq *= y;

            total = xsq;
            total *= ysq;

            if (iter >= MAX_ITER) {
                total = 5;
            };
        }; 

        clr = iter;
        clr *= 255;
        clr /= MAX_ITER;

        if (clr > 1) {
            out(clr);
        };

        out(px);
        
        pixel(px, py, &color(100));
        update();

        py += 1;
    };
    out(px);
};