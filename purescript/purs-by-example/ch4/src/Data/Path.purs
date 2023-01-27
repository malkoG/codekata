module Data.Path
  ( Path(..)
  , root
  , bin
  , ls
  , filename
  , isDirectory
  , size
  , onlyFiles
  ) where

import Data.Maybe
import Prelude

import Control.Alternative (guard)

import Data.Array ((:))
import Data.Maybe (Maybe(..))

data Path
  = Directory String (Array Path)
  | File String Int

instance showPath :: Show Path where
  show = filename


bin :: Path
bin =  Directory "/bin/"
  [ File "/bin/cp" 24800
  , File "/bin/ls" 34700
  , File "/bin/mv" 20200
  ]

root :: Path
root =
  Directory "/"
    [
      bin
    , Directory "/etc/"
        [ File "/etc/hosts" 300
        ]
    , Directory "/home/"
        [ Directory "/home/user/"
            [ File "/home/user/todo.txt" 1020
            , Directory "/home/user/code/"
                [ Directory "/home/user/code/js/"
                    [ File "/home/user/code/js/test.js" 40000
                    ]
                , Directory "/home/user/code/haskell/"
                    [ File "/home/user/code/haskell/test.hs" 5000
                    ]
                ]
            ]
        ]
    ]

filename :: Path -> String
filename (File name _) = name
filename (Directory name _) = name

isDirectory :: Path -> Boolean
isDirectory (Directory _ _) = true
isDirectory _ = false

ls :: Path -> Array Path
ls (Directory _ xs) = xs
ls _ = []

size :: Path -> Maybe Int
size (File _ bytes) = Just bytes
size _ = Nothing


allFiles' :: Path -> Array Path
allFiles' file = file : do
  child <- ls file
  allFiles' child


checkIsFile :: Path -> Boolean
checkIsFile (Directory _ _) = false
checkIsFile (File _ _) = true


onlyFiles :: Path -> Array Path
onlyFiles xs = do
  path <- allFiles' xs
  guard $ checkIsFile path

  pure path
