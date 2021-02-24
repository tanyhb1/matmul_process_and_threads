(TeX-add-style-hook
 "report"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "hmargin=1in" "vmargin=1in") ("parskip" "parfill") ("xcolor" "usenames" "dvipsnames")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "fancyhdr"
    "amsmath"
    "esint"
    "amsfonts"
    "amsthm"
    "amssymb"
    "caption"
    "subcaption"
    "amsbsy"
    "verbatim"
    "eucal"
    "mathrsfs"
    "geometry"
    "parskip"
    "listings"
    "titling"
    "graphicx"
    "xcolor")
   (LaTeX-add-labels
    "fig: mm_seq and mm_openmp"))
 :latex)

