(defproject parser "0.1.0-SNAPSHOT"
  :description "A parser for the Prose language"
  :url "https://github.com/noaht2/prose"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [cheshire "5.10.0"]]
  :repl-options {:init-ns parser.core}
  :main parser.core
  :aot [parser.core])
