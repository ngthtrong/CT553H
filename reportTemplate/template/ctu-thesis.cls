\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{template/ctu-thesis}[2026/10/21 CTU Software Engineering graduation thesis]
\RequirePackage{iftex}
\ifXeTeX\else
  \ClassError{ctu-thesis}{XeLaTeX is required}{Run make content in the template directory}
\fi
\DeclareOption{twoside}{\def\TwoSidedReport{1}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrreprt}}
\ProcessOptions\relax
% geometry owns final margins; explicit DIV avoids the initial 13bp DIV warning.
\PassOptionsToPackage{usegeometry,DIV=12}{typearea}
\ifdefined\TwoSidedReport
  \PassOptionsToClass{twoside}{scrreprt}
\else
  \PassOptionsToClass{oneside}{scrreprt}
\fi
\LoadClass[fontsize=13bp,a4paper,open=any,chapterprefix=false,
  listof=totoc,bibliography=totoc,numbers=endperiod,
  toc=chapterentrywithdots]{scrreprt}
% Faculty template margins: left 3.5 cm, right 2 cm, top/bottom 3 cm.
\RequirePackage[reset,a4paper,left=3.5cm,right=2cm,top=3cm,bottom=3cm,
  headheight=21bp,headsep=8mm,footskip=12mm]{geometry}
\ifdefined\TwoSidedReport
  \geometry{reset,a4paper,left=3.5cm,right=2cm,top=3cm,bottom=3cm,
    asymmetric,headheight=21bp,headsep=8mm,footskip=12mm}
\fi

% Headings: chapter/part titles centred and uppercase (typed in uppercase in the
% sources), sections and below left-aligned and numbered 1.1., 1.1.1.
\addtokomafont{disposition}{\rmfamily}
\setkomafont{chapter}{\normalfont\bfseries\fontsize{14bp}{18bp}\selectfont}
\setkomafont{section}{\normalfont\bfseries\fontsize{14bp}{18bp}\selectfont}
\setkomafont{subsection}{\normalfont\bfseries\fontsize{13bp}{17bp}\selectfont}
\setkomafont{subsubsection}{\normalfont\bfseries\itshape\fontsize{13bp}{17bp}\selectfont}
\setkomafont{caption}{\normalfont\normalsize}
\setkomafont{captionlabel}{\normalfont\bfseries}
\renewcommand*{\raggedchapter}{\centering}
\RedeclareSectionCommand[beforeskip=0pt,afterskip=18bp,afterindent=true]{chapter}
\RedeclareSectionCommand[beforeskip=12bp plus 2bp minus 1bp,afterskip=6bp plus 1bp,
  afterindent=true]{section}
\RedeclareSectionCommand[beforeskip=10bp plus 2bp minus 1bp,afterskip=4bp plus 1bp,
  afterindent=true]{subsection}
\RedeclareSectionCommand[beforeskip=8bp plus 2bp minus 1bp,afterskip=3bp plus 1bp,
  afterindent=true]{subsubsection}
% A break point before each heading lets chains of empty template headings split
% across pages instead of producing an overfull page.
\newcommand{\ThesisHeadingBreak}{\par\penalty0\relax}
\AddtoDoHook{heading/preinit/section}{\ThesisHeadingBreak}
\AddtoDoHook{heading/preinit/subsection}{\ThesisHeadingBreak}
\AddtoDoHook{heading/preinit/subsubsection}{\ThesisHeadingBreak}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}
\setcapindent{0pt}
\renewcommand*{\captionformat}{\ }
\KOMAoptions{captions=tableheading}

\renewcommand*{\chapterformat}{\chapapp\nobreakspace\thechapter:\enskip}

% "PART 2. CONTENT" is printed above the first chapter of the part on the same
% page, and gets its own table-of-contents line before that chapter's line.
\def\ThesisPartLabel{}
\newcommand{\ThesisPart}[1]{\gdef\ThesisPartLabel{#1}}
\let\ThesisOriginalChapterLines\chapterlinesformat
\renewcommand{\chapterlinesformat}[3]{%
  \ifx\ThesisPartLabel\@empty\else
    {\usekomafont{chapter}\ThesisPartLabel\par}\vspace{12bp}%
    \global\let\ThesisPartLabel\@empty
  \fi
  \ThesisOriginalChapterLines{#1}{#2}{#3}}
\let\ThesisOriginalChapterTocEntry\addchaptertocentry
\renewcommand*{\addchaptertocentry}[2]{%
  \ifx\ThesisPartLabel\@empty\else
    \ThesisOriginalChapterTocEntry{}{\ThesisPartLabel}%
  \fi
  \ThesisOriginalChapterTocEntry{}{\ifx\@empty#1\@empty\else
    \chapapp\nobreakspace#1:\space\fi#2}}

% Contents/lists: plain entries with dotted leaders. numbers=endperiod already puts the
% dot after every number; the figure/table format only adds the label before it.
\newcommand*{\ThesisFigureNumber}[1]{\figurename\nobreakspace#1}
\newcommand*{\ThesisTableNumber}[1]{\tablename\nobreakspace#1}
\setkomafont{chapterentry}{\normalfont}
\setkomafont{chapterentrypagenumber}{\normalfont}
\AtBeginDocument{%
  \DeclareTOCStyleEntry[indent=0pt]{tocline}{chapter}%
  \DeclareTOCStyleEntry[indent=1.5em,dynnumwidth]{tocline}{section}%
  \DeclareTOCStyleEntry[indent=3.5em,dynnumwidth]{tocline}{subsection}%
  \DeclareTOCStyleEntry[indent=6em,dynnumwidth]{tocline}{subsubsection}%
  \DeclareTOCStyleEntry[indent=0pt,dynnumwidth,entrynumberformat=\ThesisFigureNumber]{tocline}{figure}%
  \DeclareTOCStyleEntry[indent=0pt,dynnumwidth,entrynumberformat=\ThesisTableNumber]{tocline}{table}%
}

% Running header/footer follow the faculty template: thesis title in the header,
% author and ID in the footer left, page number at the footer right. Front pages
% before the table of contents carry only a centred page number.
\RequirePackage[headsepline=.4pt,footsepline=.4pt]{scrlayer-scrpage}
\clearpairofpagestyles
\setkomafont{pageheadfoot}{\normalfont\normalsize}
\setlength{\footheight}{21bp}
\defpairofpagestyles{thesis}{%
  \clearpairofpagestyles
  \lehead{\ThesisRunningTitle}\lohead{\ThesisRunningTitle}%
  \lefoot{\StudentName\ \StudentId}\lofoot{\StudentName\ \StudentId}%
  \refoot{\pagemark}\rofoot{\pagemark}}
\defpairofpagestyles{thesisplain}{%
  \clearpairofpagestyles
  \cfoot*{\pagemark}%
  \KOMAoptions{headsepline=false,footsepline=false}}
\renewcommand*{\chapterpagestyle}{thesis}
\pagestyle{thesis}
