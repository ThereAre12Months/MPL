let paddleA 190;

let ballX 320;
let ballY 240;

let ballSX 2;
let ballSY 2;

let score 0;

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

    text(&toStr(score), 320, 10, &color(0), "center");

    // -------------------------------------------

    ballX += ballSX;
    ballY += ballSY;

    if (ballY > 460) {
        ballSY -= 4;
    };

    if (ballY < 20) {
        ballSY += 4;
    };

    if (ballX > 585) {
        ballSX -= 4;
    };

    if (ballX < 55) {
        if (ballY > paddleA) {
            let end paddleA;
            end += 200;
            if (ballY < end) {
                ballSX += 4;
            };
        };
    };

    if (ballX < 40) {
        score += 1;
        ballX = 320;
    };

    update();
    fps(60);
};