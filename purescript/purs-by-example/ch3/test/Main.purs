module Test.Main where

import Prelude

import Data.AddressBook (AddressBook, Entry, emptyBook, findEntryByStreet, isInBook, removeDuplicates, (++))
import Data.Maybe (fromMaybe)
import Effect (Effect)
import Test.Unit (suite, test)
import Test.Unit.Assert as Assert
import Test.Unit.Main (runTest)


book :: AddressBook
book = { firstName: "John", lastName: "Maria", address: { street: "hello", state: "world", city: "Fake city" } }
  ++ { firstName: "Johnson", lastName: "Maria", address: { street: "hello", state: "world", city: "Fake city" } }
  ++ { firstName: "John", lastName: "Maria", address: { street: "detroit", state: "world", city: "Fake city" } }
  ++ { firstName: "John", lastName: "Maria", address: { street: "queens", state: "world", city: "Fake city" } }
  ++ { firstName: "John", lastName: "Maria", address: { street: "new york", state: "world", city: "Fake city" } }
  ++ { firstName: "John", lastName: "Maria", address: { street: "new york", state: "world", city: "Fake city" } }
  ++ { firstName: "John", lastName: "Maria", address: { street: "", state: "world", city: "Fake city" } }
  ++ { firstName: "John", lastName: "Maria", address: { street: "hello", state: "world", city: "Fake city" } }
  ++ emptyBook

emptyEntry :: Entry
emptyEntry =
  { firstName: ""
  , lastName: ""
  , address:
    { street: ""
    , state: ""
    , city: ""
  }
}

main :: Effect Unit
main = do
  runTest do
-- ANCHOR: findEntryByStreet
    suite "findEntryByStreet" do
      test "find by street name 'detroit' " do
        let
          result :: Entry
          result = fromMaybe emptyEntry $ findEntryByStreet "detroit" book
        do
          Assert.equal "detroit" (result.address.street)
      test "find by street name 'queens' "  do
        let
          result :: Entry
          result = fromMaybe emptyEntry $ findEntryByStreet "queens" book
        do
          Assert.equal "queens" (result.address.street)
      test "find by unknown street name" do
        let
          result :: Entry
          result = fromMaybe emptyEntry $ findEntryByStreet "nowhere" book
        do
          Assert.equal "" (result.address.street)

    -- ANCHOR: isInBook
    suite "isInBook" do
      test "Searching for John" do
        Assert.equal true (isInBook "John" book)
      test "Searching for Maria" do
        Assert.equal true (isInBook "Maria" book)
      test "Searching for missing name" do
        Assert.equal false (isInBook "Missing No." book)

