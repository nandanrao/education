(TeX-add-style-hook
 "summary"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("biblatex" "backend=biber" "citestyle=authoryear") ("algpseudocode" "noend")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art12"
    "mathtools"
    "amsfonts"
    "amssymb"
    "amsmath"
    "bm"
    "commath"
    "multicol"
    "algorithmicx"
    "tkz-graph"
    "algorithm"
    "fancyhdr"
    "pgfplots"
    "fancyvrb"
    "amsthm"
    "csquotes"
    "booktabs"
    "biblatex"
    "algpseudocode")
   (LaTeX-add-bibliographies))
 :latex)

