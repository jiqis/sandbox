let counter = ref 0

let rec produce (id,i) =
  if i>0 then (pl := (!counter)::(!pl);
               inc ();
               produce (id,i-1))
  else ()
let rec c_thread threads n i =
  if i<n then c_thread ((Thread.create produce (i,10))::threads) n (i+1)
  else threads
let rec j_thread threads =
  match threads with
    [] -> ()
  | p::ps -> (Thread.join p;
              j_thread ps)
let print_list pl =
  let l = !pl in
  let rec sub_print_list = function
    [] -> ()
  | x::xs -> (print_int x;
              sub_print_list xs) in
  sub_print_list l

let () =
  let threads = c_thread [] 10 0 in
  j_thread threads;
  print_list pl
  
  
