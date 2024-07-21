open Cis194;;
open Hw1;;

assert (last_digit 12345 = 5);;
assert (last_digit 0 = 0);;

assert (to_digits 12345 = [1;2;3;4;5]);;
assert (to_digits 0 = []);;
assert (to_digits (-17) = []);;

assert (double_every_other [1;2] = [2;2]);;
assert (double_every_other [2;1] = [4;1]);;
assert (double_every_other [1;2;3] = [1;4;3]);;
assert (double_every_other [8;7;6;5] = [16;7;12;5]);; 


assert (sum_digits [16;7;12;5] = 1 + 6 + 7 + 1 + 2 + 5);;

assert (validate 4012888888881881 = true);;
assert (validate 4012888888881882 = false);;
