module Data.AddressBook where

import Data.Maybe
import Prelude

import Control.Plus (empty)
import Data.List (List(..), filter, head, null)

type Entry =
  { firstName :: String
  , lastName :: String
  , address :: Address
  }

type Address =
  { street :: String
  , city   :: String
  , state  :: String
  }

type AddressBook = List Entry

showEntry :: Entry -> String
showEntry entry =
  entry.lastName <> ", " <>
  entry.firstName <> ": " <>
  showAddress entry.address


showAddress :: Address -> String
showAddress addr =
  addr.street <> ", " <>
  addr.city <> ", " <>
  addr.state


emptyBook :: AddressBook
emptyBook = empty -- this means empty list


insertEntry :: Entry -> AddressBook -> AddressBook
insertEntry = Cons


findEntry :: String -> String -> AddressBook -> Maybe Entry
findEntry firstName lastName = head <<< filter filterEntry
  where
    filterEntry :: Entry -> Boolean
    filterEntry entry = entry.firstName == firstName && entry.lastName == lastName


findEntryByStreet :: String -> AddressBook -> Maybe Entry
findEntryByStreet street = head <<< filter filterEntry
  where
    filterEntry :: Entry -> Boolean
    filterEntry = eq street <<< _.address.street


isInBook :: String -> AddressBook -> Boolean
isInBook name = not null <<< filter filterEntry
  where
    filterEntry :: Entry -> Boolean
    filterEntry entry = entry.firstName == name || entry.lastName == name


removeDuplicates :: AddressBook -> AddressBook
removeDuplicates book = book


infixr 5 insertEntry as ++


