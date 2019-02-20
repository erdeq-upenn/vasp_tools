
print r'''
\documentclass{article}
\usepackage{titlesec}
\usepackage[top=2.0cm, bottom=1.5cm, left=2.5cm, right=2.5cm]{geometry}
\usepackage{ragged2e}
\usepackage{pdfpages}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{makeidx}
\usepackage{graphicx}
\usepackage{titlesec}
\usepackage{tikz}
\usepackage{fancyhdr}
\usepackage{lastpage}
%\usepackage{ulem}
\usepackage[normalem]{ulem}
\usepackage{hyperref}
\usepackage{times}
\usepackage{color}
\usepackage{multirow}
%\usepackage{colortbl}

%\fontsize{26pt}{1.2pt}
%\selectfont

\usepackage{times}

\usepackage{titlesec, blindtext, color}
\definecolor{gray75}{gray}{0.75}
\newcommand{\hsp}{\hspace{10pt}}
%\titleformat{\chapter}[hang]{\Huge\bfseries}{Exhibit \thechapter\hsp\textcolor{gray75}{|}\hsp}{0pt}{\Huge\bfseries}
%\titleformat{\section}[hang]{\Large\bfseries}{Exhibit \thesection\hsp\textcolor{gray75}{|}\hsp}{0pt}{\Large\bfseries}


\begin{document}

\author{Junwen Li}
\title{Application}
\date{August 2012}

%\thispagestyle{empty}

\setcounter{page}{1}
'''

def output_pdf(efield):
    print r"\includepdf[page=1,scale=0.95]{" + "%.2f" % (efield) + r"-p/bands/bands.pdf}"
        
print r"\clearpage"
#print r"\includepdfset[pages=]}"
for i in range(0,38,2):
    output_pdf(i/100.0)


print r"\end{document}"
