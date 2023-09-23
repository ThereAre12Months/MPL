# MPL
MPL or "My Programming Language" is a programming language created by PatattMan.
Below you can see how the programming language works.

You can find an online code editor for mpl at <https://thereare12months.github.io/MPL> and examples under the [examples](/examples/) folder.

## Sections
1. [Variables](#variables)  
1.1 [Variable declaration](#variable-declaration)  
1.2 [Variable manipulation](#variable-manipulation)  
1.3 [Variable accessing](#variable-accessing)
2. [Functions](#functions)  
2.1 [Built-ins](#built-ins)  
2.2 [Creating custom functions](#creating-custom-functions)  
2.3 [Calling custom functions](#calling-custom-functions)
3. [Loops](#loops)  
3.1 [While](#while-loops)  
3.2 [Until](#until-loops)  
3.3 [Repeat](#repeat-loops)  
3.4 [Loop](#loop-loops)  
3.5 [Froot loops](#froot-loops)
4. [Conditionals](#conditionals)  
4.1 [If](#if-statement)
5. [Graphics](#graphics)  
5.1 [Basics](#basics)  
5.2 [Simple shapes](#simple-shapes)  
5.3 [Images](#images)

## Variables
### Variable Declaration
You can create variables with the `let` keyword, followed by the name of the variable and then its starting value.
Eg. `let age 25;`

Variables can be many different types including: `int`, `float`, `string`, `array` and `codeblock`.  
The last one may surprise you as it is not found in many other programming languages. It is simply, as the name infers, a block of code.
```rust
// example of a code block
let code_block { 
    let name in("What's your name? ");
    out(("Hello " + name + "!"));
};

code_block();
```
Codeblocks can be seen as functions without arguments.

To indicate the type of the value being given to the variable certain annotations can be used.
```rust
integers:   let age 23;
floats:     let pi f3.1415;
strings:    let state "Colorado";
arrays:     let colors ["red", "green", "blue"];
codeblocks  let hello { out("Hello world!"); };
```

The scope where a variable is created matters. Variables created in the `main` scope are `global` and can be used everywhere in the code. Variables created in any other scope are `local` and can only be used in its specific scope.

### Variable manipulation
Variables can be manipulated in many ways like other languages.

Two variables can switch their values using the `<->` keyword.  
Eg. `a <-> b;`  
This causes `a` to take the value of `b` and vice versa.

A variable can be set again to a new value.  
Eg. `a = 53;`

A variable can also be manipulated by basic maths:
```
a += 5;
a -= b;
a *= f1.125;
a /= 19;
```

### Variable accessing
Variables can be accesed everywhere (in their designated scope).  
In functions: `out(("Hello " + name));`  
In conditions: `if (age < 18) {...};`  
And basically everywhere else.

## Functions
### Built-ins
Built-ins are immutable in MPL, therefore you can't assign a new function/value to an existing function. Built-ins can be called by typing its name and the arguments in brackets.  
Eg. `out("This is an argument");`

You can also include other functions as arguments to a function. You can do this by referencing the function with the ampersand (&).  
Eg. `parseAnswer(&in("Do you want to continue? "));`

### Creating custom functions
Custom functions can be created with the `fn` keyword followed by the name of the function its arguments and the codeblock.
```rust
fn sayYourName(name) {
    out(("Nice to meet you " + name + "!"));
};
```
Functions can have multiple named arguments that can be used like any variable in the code.  
Optional arguments are not implemented yet.

### Calling custom functions
Calling custom functions works just like calling built-in functions: `nameOfFunction(arg1, arg2);`.

## Loops
### While loops
While loops consist of the `while` keyword, a condition (eg. `(name == "Bernie")`) and a codeblock.

While loops run as long as the condition is met. Once the condition is no longer true the loop stops.
```rust
let value 1;
while (value < 1000) {
    value *= 2;
    out(value);
};
```
Note that variables created inside of a while loop are considered local variables and cannot be used outside of said while loop.

### Until loops
Until loops function just like while loops. In fact it even uses the same syntax. But instead of repeating the code **as long as** the condition is met, it repeats the code **until** the condition is met. Therefore once the condition is met the loop stops.
```rust
let value 1;
until (value >= 1000) {
    value *= 2;
    out(value);
};
```
Just as in the while loop variables created inside of an until loop are local.

### Repeat loops
Repeat loops repeat over certain code a specific amount of time.
```rust
repeat 15 {
    out("This code gets executed 15 times");
};
```
And once again variables created inside the repeat loop are local.

### Loop loops
Loop loops are simply loops that run indefinitely. In the current version of MPL there is no way to exit the loop except crashing/exiting the program (a nicer way is coming).
```rust
loop {
    out("This will never stop!")
};
```
Like all the other loops variables created inside of the loop are local (not that it matters since you won't be executing any code after that).

### Froot loops
Just kidding I haven't implemented nor am I planning to implement froot loops. (or am I????)

## Conditionals
### If statement
You can create if statements by using the `if` keyword followed by a condition and a codeblock.
```rust
if (mood == "singing") {
    out("If you're happy and you know it clap your hands. clap clap...");
};
```
And like I have said many times before, variables created inside of an if statement are local.

Elif/else are yet to be implemented.

## Graphics

**Note that graphics don't work with the online terminal.**

### Basics

In MPL you can create a new window with the `setup()` function. The `setup()` function takes 2 arguments: the intitial width and height of the window.
You can also change the title of the window with the `title()` function with the new title as the only argument. 

A lot of functions that draw something onto the window need a color argument. For that there is a specific color datatype that can be created by using the `color()` function. Eg. `circle(x, y, r, &color(0, 255, 255));` or `let color color(255);`

Clearing the screen is done by 

### Simple shapes

Drawing single pixels : `pixel(x, y, color);`  
Drawing circles       : `circle(x, y, r, color);`  
Drawing rectangles    : `rect(x, y, w, h, color);`  
Drawing lines         : `line(x1, y1, x2, y2, w, color);`  

### Images

You can load images with the `loadImg()` function. Simply give the path to the image as argument.  
Eg. `let playerImg loadImg("assets/imgs/player.png");`

Blitting the image to the main window is done with the `blit()` function.   
Eg. `blit(img, x, y);`