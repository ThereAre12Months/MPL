setup(640, 480);
title("Follow the mouse");

loop {
    fill(&color(255));
    circle(&mouseX(), &mouseY(), 10, &color());
    update();
};
