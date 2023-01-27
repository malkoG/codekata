module Test.Main where

import Prelude

import Data.Array (length)
import Data.Maybe (fromMaybe)
import Data.Path (Path(..), bin, onlyFiles, root)
import Effect (Effect)
import Test.Unit (suite, test)
import Test.Unit.Assert as Assert
import Test.Unit.Main (runTest)
import Util (allTrue, cartesianProduct, countEven, isEven, keepNonNegative, primeFactors, reversel, squared, triples)



main :: Effect Unit
main = do
  runTest do
    -- ANCHOR: isEven
    suite "isEven" do
      test "0 is even " do
        Assert.equal true (isEven 0)
      test "1 is not even "  do
        Assert.equal false (isEven 1)
      test "2 is even" do
        Assert.equal true (isEven 2)
      test "10 is even" do
        Assert.equal true (isEven 10)

    -- ANCHOR: countEven
    suite "countEven" do
      test "[1,2,3,4,5] has 2 even number" do
        Assert.equal 2 (countEven [1,2,3,4,5])
      test "[2,4,6,8,10] has 5 even number" do
        Assert.equal 5 (countEven [2,4,6,8,10])

    -- ANCHOR: squared
    suite "squared" do
      test "[1,2,3,4,5]" do
        Assert.equal [1,4,9,16,25] (squared [1,2,3,4,5])
      test "[2,4,6,8,10]" do
        Assert.equal [4,16,36,64,100] (squared [2,4,6,8,10])

    -- ANCHOR: keepNonNegative
    suite "countEven" do
      test "[-1,2,-3,4,-5]" do
        Assert.equal [2,4] (keepNonNegative [-1,2,-3,4,-5])
      test "[2,-4,6,-8,10]" do
        Assert.equal [2,6,10] (keepNonNegative [2,-4,6,-8,10])


    -- ANCHOR: catesianProduct
    suite "catesianProduct" do
      test "passing [1,2], [3,4] retuns [[1,3],[1,4],[2,3],[2,4]]" do
        Assert.equal [[1,3],[1,4],[2,3],[2,4]] (cartesianProduct [1,2] [3,4])

    -- ANCHOR: triples
    suite "triples" do
      test "passing 5 returns [[3,4,5]]" do
        Assert.equal [[3,4,5]] (triples 5)
      test "passing 13 returns [[3,4,5],[5,12,13],[6,8,10]]" do
        Assert.equal [[3,4,5],[5,12,13],[6,8,10]] (triples 13)

    -- ANCHOR: primeFactors
    suite "primeFactors" do
      test "passing 5 returns [5]" do
        Assert.equal [5] (primeFactors 5)
      test "passing 6 returns [2,3]" do
        Assert.equal [2,3] (primeFactors 6)
      test "passing 12 returns [2,3]" do
        Assert.equal [2,3] (primeFactors 12)
      test "passing 36 returns [2,3]" do
        Assert.equal [2,3] (primeFactors 36)


    -- ANCHOR: allTrue
    suite "allTrue" do
      test "passing [] returns true" do
        Assert.equal true (allTrue [])
      test "passing [true,true] returns true" do
        Assert.equal true (allTrue [true, true])
      test "passing [true,false] returns false" do
        Assert.equal false (allTrue [true, false])

    -- ANCHOR: reversel
    suite "reversel" do
      test "passing [1,2,3,4,5] returns [5,4,3,2,1]" do
        Assert.equal [5,4,3,2,1] (reversel [1,2,3,4,5])
      test "passing ['c', 'b', 'a'] returns ['a', 'b', 'c']" do
        Assert.equal ["a", "b", "c"] (reversel ["c", "b", "a"])


    -- ANCHOR: onlyFiles
    suite "onlyFiles" do
      test "passing root returns 7" do
        Assert.equal 7 (length $ show <$> onlyFiles root)
      test "passing bin returns 3" do
        Assert.equal 3 (length $ show <$> onlyFiles bin)


