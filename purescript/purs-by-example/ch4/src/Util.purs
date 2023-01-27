module Util where

import Data.Maybe
import Prelude

import Control.Alternative (guard)
import Control.Plus (empty)
import Data.Array (concatMap, filter, head, tail, length, (..))
import Data.Foldable (foldr, foldl)
import Data.List (List(..), null)


isEven :: Int -> Boolean
isEven 0 = true
isEven 1 = false
isEven n = not $ isEven (n - 1)


countEven :: Array Int -> Int
countEven [] = 0
countEven xs =
  result + (countEven $ fromMaybe [] $ tail xs)
  where
    result = if isEven $ fromMaybe 0 $ head xs then 1 else 0


squared :: Array Int -> Array Int
squared xs = (\x -> x * x) <$> xs


keepNonNegative :: Array Int -> Array Int
keepNonNegative xs = filter (\x -> x > 0) xs


factors :: Int -> Array (Array Int)
factors n = do
  i <- 1 .. n
  j <- i .. n
  guard $ i * j == n
  pure [i, j]


cartesianProduct :: Array Int -> Array Int -> Array (Array Int)
cartesianProduct xs ys = do
  x <- xs
  y <- ys
  pure [x, y]


triples :: Int -> Array (Array Int)
triples n = do
  a <- 1 .. n
  b <- 1 .. n
  c <- 1 .. n

  guard $ c * c == a * a + b * b && a < b && b < c
  pure [a, b, c]


isPrime :: Int -> Boolean
isPrime n = eq 1 (length $ factors n)


primeFactors :: Int -> Array Int
primeFactors n = do
  i <- 2 .. n
  guard $ n `mod` i == 0 && isPrime i
  pure i


allTrue :: Array Boolean -> Boolean
allTrue = foldl (\acc x -> acc && x ) true

reversel :: forall a. Array a -> Array a
reversel = foldl (\xs x -> [x] <> xs) []
