---
title: "\"Clean Architecture: A Craftsman's Guide to Software Structure and Design\" 1 - Introduction and Programming Paradigms"
layout: post
tags:
  - book
---

This post is a note for Part I (Introduction), and Part II (Programming Paradigms) in [*Clean Architecture: A Craftsman's Guide to Software Structure and Design* by Robert C. Matrin](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164).

## Introduction

### 1. What is Design and Architecture?

* **NO DIFFERENCES BETWEEN THEM**
* Usually "architecture" means structure at a high-level, and "design" means structure at a low-level. But Low-level details (design) and the high-level structure (architecture) are all part of the software design.
* ***The goal of software architecture is to minimize the human resources required to build and maintain the required system.***
* Design quality can be measured by the effort. If required effort is high, the design is bad.
* The best option in every case is **to recognize and avoid its overconfident** and **to start taking the quality of software architecture seriously**.

### 2. A Tale of Two Values.

* Two values: **behavior**, **structure**
* *The first value of software -behavior- is urgent but not always particularly important.*
* *The second value of software -architecture- is important but never particularly urgent.*
* Both things should be remained high, but we can arrange works into these four priorities.
    1. Urgent and important
    1. Not urgent and important
    1. Urgent and not important
    1. Not urgent and not important
* ***Note that the architecture of the code is in the top two positions.***
* *The responsibility of software developers is to assert the importance of architecture over the urgency of features.*

## Starting With The Bricks: Programming Paradigms

* Paradigms: the ways of programming, relatively unrelated to languages.
* A paradigm tells you which programming structures to use, and when to use them.

### 3. Paradigm Overview

* three paradaigms: **Structured Programming**, **Object-Orient Programming**, and **Functional Programming**.
* Note: Each of the paradigms ***removes*** capabilities from the programmer. None of them adds new capabilities.

### 4. Structured Programming

* Why was Structured Programming born? All programs can be built with a minimum set of control structures. (sequence, selection, and iteration)
* Structured Programming allows modules to be recursively decomposed into provable units, so we can decompose a large-scale problem into high-level functions. And each of those functions can be decomposed into lower-level functions.
* > "Testing shows the presence, not the absence, of bugs" by Dijkstra.

### 5. Object-Oriented Programming

* Three magic words for Object-Oriented: *encapsulation*, *inheritance*, and *polymorphism*
* Encapsulation makes data to be hidden and required function to be shown.
* Inheritance is simply the redeclaration of a group of variables and functions within an enclosing scope.
  * Encapsulation does not make OO great itself, and perhaps inheritance can make OO better.
* Polymorphism helps OO to allow the plugin architecture to be used anywhere.
  * In traditional software architecture, source code dependencies should follow the flow of control.
  * **But OO languages provide safe and convenient polymorphism, so source code dependencies can be inverted.** (Dependency Inversion)
* ***OO is the ability, through the use of polymorphism, to gain absolute control over every source code dependency in the system.***

### 6. Functional Programming

* Other programming languages are using a mutable variable as a loop control variable, but in functional languages no such mutable variable exists.
  * Because all race conditions, deadlock conditions, and concurrent issues are due to mutable variables.
* **Segregation of Mutability**
  * One of the most common compromises in regard to immutability is to segregate the application into mutable and immutable components.
  * Architects would be wise to push as much processing as possible into the immutable components.
* **Event Sourcing**
  * Event sourcing is a strategy wherein we store the transactions, but not the state. (In bank applications, imagine that storing transactions instead of balance.)
  * Then, nothing ever gets deleted or updated from such a data store. As a consequence, our applications are not CRUD; they are just CR.
  * If we have enough storage and process power, we can make our applications entirely immutable and functional.
