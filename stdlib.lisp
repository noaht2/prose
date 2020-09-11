#!/home/noaht2/prose/prose.sh
(list
 (def lambda2fn1 (lambda app (lambda arg (app (eval arg)))))
 ((lambda2fn1 (lambda x (+ x 1))) (+ 1 1))
 (def add2 (lambda2fn1 (lambda n (lambda m (+ m (* 2 n))))))
 (add2 (+ 1 1) (+ 1 1)))
