setup(640, 480);
title("All colors!");

let red 0;
let green 0;
let blue 0;
repeat 256 {
    green = 0;
    repeat 256 {
        blue = 0;
        repeat 256 {
            fill(&color(red, green, blue));
            blue += 1;
        };
        green += 1;
    };
    red += 1;
};