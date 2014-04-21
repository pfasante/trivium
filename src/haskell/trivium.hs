module Trivium (encrypt, decrypt, keystream) where

import Control.Monad(forM_)
import Control.Monad.ST.Safe (runST)
import Data.StateRef
import Data.Bits (xor)

--data TState

encrypt :: Integer -> Integer -> [Int] -> [Int]
encrypt key iv pt = zipWith xor pt (keystream key iv (length pt))

decrypt :: Integer -> Integer -> [Int] -> [Int]
decrypt = encrypt

keystream :: Integer -> Integer -> Int -> [Int]
keystream key iv cnt = runST $ do
    n <- newReference []
    forM_ [1..cnt] $ \_ ->
        modifyRef n (1:)
    readRef n