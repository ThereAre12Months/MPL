// pong written in mpl

let paddleA 190;

let ballX 320;
let ballY 240;

setup(640, 480);
title("Pong!");

loop {
    fill(&color(255));

    paddleA = &mouseY();
    paddleA -= 100;

    rect(5, paddleA, 30, 200, &color(0));
    circle(ballX, ballY, 20, &color(0));

    let paddleB 0;

    paddleB = ballY;
    paddleB -= 100;

    rect(605, paddleB, 30, 200, &color(0));

    update();
};