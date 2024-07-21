
let last_digit n = n mod 10;;
let drop_last_digit n = n / 10;;

let to_digits n = 
  let rec to_digits' n acc = 
    if n <= 0 then acc
    else to_digits' (drop_last_digit n) ((last_digit n)::acc)
  in to_digits' n [];;

let double_every_other'' lst = 
  let rec double_every_other' lst acc = 
    match lst with
    | [] -> acc
    | [x] -> x::acc
    | x::y::tl -> double_every_other' tl (y*2::x::acc)
  in double_every_other' lst [];;

let double_every_other lst = 
  (double_every_other'' (List.rev lst));;


let sum_digits lst = 
  List.fold_left (fun acc x -> acc + (List.fold_left (fun acc y -> acc + y) 0 (to_digits x))) 0 lst;;


let validate n = 
  let digits = to_digits n in
  let doubled = double_every_other digits in
  let sum = sum_digits doubled in
  sum mod 10 = 0;;
