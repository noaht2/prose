 (def lambda2fn1 (lambda app (lambda arg (app, (eval arg)))))
 ((lambda2fn1 (lambda x (+ x 1))) ("+", "1", "1"))
 (def 2add (lambda2fn1 (lambda n (lambda m (+ (* 2 n) m)))))
 (2add (+ 1 1) (+ 1 1)))
