#!/bin/bash
sudo apt update
npm install -g typescript
sudo apt install --assume-yes rustc
git clone https://github.com/lf-lang/lingua-franca.git --branch master --depth 1
cd lingua-franca
./gradlew buildAll
cd ..
git clone https://github.com/lf-lang/examples-lingua-franca.git examples --branch main
