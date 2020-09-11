(ns parser.core
  (:gen-class)
  (:require [cheshire.core :refer :all]))

(defmulti rm-clj class)

(defmethod rm-clj java.lang.Long [code]
  (str code))

(defmethod rm-clj java.lang.String [code]
  (str "\"" code "\""))

(defmethod rm-clj clojure.lang.Symbol [code]
  (str code))

(defmethod rm-clj :default [code]
  (map rm-clj code))

(defn -main [& args]
  (println
   (generate-string
    (rm-clj (read-string (apply str
                                (take-while identity (repeatedly #(.readLine *in*)))))))))
