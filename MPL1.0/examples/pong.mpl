setup(640, 480);
title("pong");

let ballX 320;
let ballY 240;

let speedX 1;
let speedY 2;

loop {
    fill(&color(255));
    circle(ballX, ballY, 20, &color());
    ballX += speedX;
    ballY += speedY;
    update();

    if (ballX > 640) {
        ballX = 0;
    };

    if (ballY > 480) {
        ballY = 0;
    };
};