module Test.Main where

import Prelude

import Solution (answer, diagonal)

import Effect (Effect)

import Test.Unit (suite, test)
import Test.Unit.Assert as Assert
import Test.Unit.Main (runTest)


main :: Effect Unit
main = do
  runTest do
-- ANCHOR: Euler
    suite "Euler - Sum of Multiples" do
      test "below 10" do
        Assert.equal 23 (answer 10)
      test "below 1000" do
        Assert.equal 233168 (answer 1000)

-- ANCHOR: diagonalTests
    suite "diagonal" do
      test "3 4 5" do
        Assert.equal 5.0 (diagonal 3.0 4.0)
      test "5 12 13" do
        Assert.equal 13.0 (diagonal 5.0 12.0)

