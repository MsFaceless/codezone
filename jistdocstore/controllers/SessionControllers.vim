let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
imap <S-Tab> 
inoremap <C-Tab> 	
inoremap <silent> <Plug>NERDCommenterInInsert  <BS>:call NERDComment(0, "insert")
vnoremap  <Nop>
nmap ,ca <Plug>NERDCommenterAltDelims
vmap ,cA <Plug>NERDCommenterAppend
nmap ,cA <Plug>NERDCommenterAppend
vmap ,c$ <Plug>NERDCommenterToEOL
nmap ,c$ <Plug>NERDCommenterToEOL
vmap ,cu <Plug>NERDCommenterUncomment
nmap ,cu <Plug>NERDCommenterUncomment
vmap ,cn <Plug>NERDCommenterNest
nmap ,cn <Plug>NERDCommenterNest
vmap ,cb <Plug>NERDCommenterAlignBoth
nmap ,cb <Plug>NERDCommenterAlignBoth
vmap ,cl <Plug>NERDCommenterAlignLeft
nmap ,cl <Plug>NERDCommenterAlignLeft
vmap ,cy <Plug>NERDCommenterYank
nmap ,cy <Plug>NERDCommenterYank
vmap ,ci <Plug>NERDCommenterInvert
nmap ,ci <Plug>NERDCommenterInvert
vmap ,cs <Plug>NERDCommenterSexy
nmap ,cs <Plug>NERDCommenterSexy
vmap ,cm <Plug>NERDCommenterMinimal
nmap ,cm <Plug>NERDCommenterMinimal
vmap ,c  <Plug>NERDCommenterToggle
nmap ,c  <Plug>NERDCommenterToggle
vmap ,cc <Plug>NERDCommenterComment
nmap ,cc <Plug>NERDCommenterComment
map -t <Plug>TaskList
map <silent> -mm :ShowMarksPlaceMark
map <silent> -ma :ShowMarksClearAll
map <silent> -mh :ShowMarksClearMark
map <silent> -mo :ShowMarksOn
map <silent> -mt :ShowMarksToggle
nnoremap -sv :source $MYVIMRC
nnoremap -ev :vsplit $MYVIMRC
noremap / :call SearchCompleteStart()/
nnoremap ;' :%s:::cg<Left><Left><Left><Left>
nnoremap ;; :%s:::g<Left><Left><Left>
nnoremap T :TaskList
nmap ]f :call PythonDec("function", 1)
nmap ]F :call PythonDec("function", -1)
nmap ]j :call PythonDec("class", 1)
nmap ]J :call PythonDec("class", -1)
nmap ]u :call PythonUncommentSelection()
nmap ]# :call PythonCommentSelection()
nmap ]> ]tV]e>
nmap ]< ]tV]e<
nmap ]e :PEoB
nmap ]t :PBoB
vmap ]f :call PythonDec("function", 1)
omap ]f :call PythonDec("function", 1)
vmap ]F :call PythonDec("function", -1)
omap ]F :call PythonDec("function", -1)
vmap ]j :call PythonDec("class", 1)
omap ]j :call PythonDec("class", 1)
vmap ]J :call PythonDec("class", -1)
omap ]J :call PythonDec("class", -1)
map ]<Down> :call PythonNextLine(1)
map ]<Up> :call PythonNextLine(-1)
map ]d :call PythonSelectObject("function")
map ]c :call PythonSelectObject("class")
vmap ]u :call PythonUncommentSelection()
omap ]u :call PythonUncommentSelection()
vmap ]# :call PythonCommentSelection()
omap ]# :call PythonCommentSelection()
vmap ]> >
omap ]> ]tV]e>
vmap ]< <
omap ]< ]tV]e<
map ]v ]tV]e
vmap ]e :PEoBm'gv``
omap ]e :PEoB
vmap ]t :PBOBm'gv``
omap ]t :PBoB
nmap gx <Plug>NetrwBrowseX
vnoremap jk 
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#NetrwBrowseX(expand("<cWORD>"),0)
nnoremap <silent> <F11> :call conque_term#exec_file()
nmap <silent> <Plug>NERDCommenterAppend :call NERDComment(0, "append")
nnoremap <silent> <Plug>NERDCommenterToEOL :call NERDComment(0, "toEOL")
vnoremap <silent> <Plug>NERDCommenterUncomment :call NERDComment(1, "uncomment")
nnoremap <silent> <Plug>NERDCommenterUncomment :call NERDComment(0, "uncomment")
vnoremap <silent> <Plug>NERDCommenterNest :call NERDComment(1, "nested")
nnoremap <silent> <Plug>NERDCommenterNest :call NERDComment(0, "nested")
vnoremap <silent> <Plug>NERDCommenterAlignBoth :call NERDComment(1, "alignBoth")
nnoremap <silent> <Plug>NERDCommenterAlignBoth :call NERDComment(0, "alignBoth")
vnoremap <silent> <Plug>NERDCommenterAlignLeft :call NERDComment(1, "alignLeft")
nnoremap <silent> <Plug>NERDCommenterAlignLeft :call NERDComment(0, "alignLeft")
vmap <silent> <Plug>NERDCommenterYank :call NERDComment(1, "yank")
nmap <silent> <Plug>NERDCommenterYank :call NERDComment(0, "yank")
vnoremap <silent> <Plug>NERDCommenterInvert :call NERDComment(1, "invert")
nnoremap <silent> <Plug>NERDCommenterInvert :call NERDComment(0, "invert")
vnoremap <silent> <Plug>NERDCommenterSexy :call NERDComment(1, "sexy")
nnoremap <silent> <Plug>NERDCommenterSexy :call NERDComment(0, "sexy")
vnoremap <silent> <Plug>NERDCommenterMinimal :call NERDComment(1, "minimal")
nnoremap <silent> <Plug>NERDCommenterMinimal :call NERDComment(0, "minimal")
vnoremap <silent> <Plug>NERDCommenterToggle :call NERDComment(1, "toggle")
nnoremap <silent> <Plug>NERDCommenterToggle :call NERDComment(0, "toggle")
vnoremap <silent> <Plug>NERDCommenterComment :call NERDComment(1, "norm")
nnoremap <silent> <Plug>NERDCommenterComment :call NERDComment(0, "norm")
nnoremap <silent> <M-Left> :tabprevious
nnoremap <silent> <M-Right> :tabnext
nnoremap <F12> :TlistToggle
nnoremap <F10> :ls:e # 
nnoremap <F7> o"""
nnoremap <F6> O"""
nnoremap <F5> @="I#j"<Left><Left>  
nnoremap <F4> :wa|exe "mksession! " . v:this_session
nnoremap <F3> :wa
nnoremap <F2> :w|!python %
imap 	 
inoremap  <Nop>
inoremap jk 
let &cpo=s:cpo_save
unlet s:cpo_save
set autoindent
set autowrite
set background=dark
set backspace=indent,eol,start
set expandtab
set fileencodings=ucs-bom,utf-8,default,latin1
set helplang=en
set hidden
set history=50
set hlsearch
set ignorecase
set incsearch
set nomodeline
set omnifunc=pythoncomplete#Complete
set path=.,/usr/include,,,/usr/local/lib/python2.7/dist-packages/SQLAlchemy-0.7.8-py2.7-linux-x86_64.egg,/usr/local/lib/python2.7/dist-packages/pyserial-2.6-py2.7.egg,/usr/local/lib/python2.7/dist-packages/PyX-0.12.1-py2.7.egg,/usr/local/lib/python2.7/dist-packages/pyzmq-13.0.2-py2.7-linux-x86_64.egg,/usr/local/lib/python2.7/dist-packages/requests-1.2.0-py2.7.egg,/usr/lib/pymodules/python2.7,/usr/local/lib/python2.7/dist-packages/python_nmap-0.2.7-py2.7.egg,/usr/local/lib/python2.7/dist-packages/pygeoip-0.2.6-py2.7.egg,/usr/local/lib/python2.7/dist-packages/mechanize-0.2.5-py2.7.egg,/usr/local/lib/python2.7/dist-packages/beautifulsoup4-4.2.1-py2.7.egg,/usr/local/lib/python2.7/dist-packages/BeautifulSoup-3.2.1-py2.7.egg,~/jistenv/jistdocstore/jistdocstore/controllers,~/code/python/scripts,/usr/local/lib64,/usr/lib/python2.7,/usr/lib/python2.7/plat-linux2,/usr/lib/python2.7/lib-tk,/usr/lib/python2.7/lib-dynload,/usr/local/lib/python2.7/dist-packages,/usr/lib/python2.7/dist-packages,/usr/lib/python2.7/dist-packages/PIL,/usr/lib/python2.7/dist-packages/gst-0.10,/usr/lib/python2.7/dist-packages/gtk-2.0,/usr/lib/python2.7/dist-packages/ubuntu-sso-client,/usr/lib/python2.7/dist-packages/ubuntuone-client,/usr/lib/python2.7/dist-packages/ubuntuone-control-panel,/usr/lib/python2.7/dist-packages/ubuntuone-couch,/usr/lib/python2.7/dist-packages/ubuntuone-installer,/usr/lib/python2.7/dist-packages/ubuntuone-storage-protocol,/usr/lib/python2.7/dist-packages/wx-2.8-gtk2-unicode
set printoptions=paper:a4
set ruler
set runtimepath=~/.vim,/var/lib/vim/addons,/usr/share/vim/vimfiles,/usr/share/vim/vim73,/usr/share/vim/vimfiles/after,/var/lib/vim/addons/after,~/.vim/after
set shiftwidth=4
set showcmd
set showmatch
set showtabline=2
set smartcase
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc
set tabpagemax=20
set tabstop=4
set textwidth=175
set wildignore=*.pyc
set window=56
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/jistenv/jistdocstore/jistdocstore/controllers
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 accountscont.py
badd +1 cctvcont.py
badd +1 contractscont.py
badd +1 est3yresshsfcont.py
badd +1 est3yresspalisadecont.py
badd +1 est5yreskomfencingcont.py
badd +1 estimatingcont.py
badd +1 invoicingcont.py
badd +7191 labourcont.py
badd +1 logisticscont.py
badd +1 managementcont.py
badd +1 manufacturecont.py
badd +155 marketingcont.py
badd +1 productioncont.py
badd +306 receptioncont.py
badd +68 tablecont.py
badd +990 transportcont.py
badd +1 vettingcont.py
badd +1 fleetcont.py
badd +0 \*upload\*
args accountscont.py cctvcont.py contractscont.py est3yresshsfcont.py est3yresspalisadecont.py est5yreskomfencingcont.py estimatingcont.py invoicingcont.py labourcont.py logisticscont.py managementcont.py manufacturecont.py marketingcont.py productioncont.py receptioncont.py tablecont.py transportcont.py vettingcont.py
edit accountscont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
35
normal zo
41
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
44
normal zo
41
normal zo
287
normal zo
295
normal zo
295
normal zo
295
normal zo
295
normal zo
295
normal zo
295
normal zo
295
normal zo
287
normal zo
381
normal zo
390
normal zo
390
normal zo
390
normal zo
390
normal zo
390
normal zo
390
normal zo
390
normal zo
407
normal zo
407
normal zo
407
normal zo
407
normal zo
407
normal zo
420
normal zo
425
normal zo
425
normal zo
425
normal zo
425
normal zo
425
normal zo
425
normal zo
425
normal zo
425
normal zo
420
normal zo
381
normal zo
474
normal zo
478
normal zo
478
normal zo
478
normal zo
478
normal zo
478
normal zo
474
normal zo
1414
normal zo
1437
normal zo
1444
normal zo
1446
normal zo
1446
normal zo
1446
normal zo
1448
normal zo
1448
normal zo
1448
normal zo
1446
normal zo
1446
normal zo
1446
normal zo
1444
normal zo
1437
normal zo
1414
normal zo
1480
normal zo
1516
normal zo
1523
normal zo
1523
normal zo
1523
normal zo
1523
normal zo
1529
normal zo
1529
normal zc
1529
normal zo
1523
normal zc
1523
normal zo
1523
normal zo
1523
normal zo
1516
normal zc
1480
normal zc
1552
normal zo
1552
normal zc
1689
normal zo
1689
normal zc
1781
normal zo
1781
normal zc
1797
normal zo
1797
normal zc
1931
normal zo
1931
normal zc
2021
normal zo
2021
normal zc
2037
normal zo
2037
normal zc
2134
normal zo
2134
normal zc
2188
normal zo
2188
normal zc
2204
normal zo
2205
normal zc
2204
normal zc
2341
normal zo
2341
normal zc
2464
normal zo
2464
normal zc
2513
normal zo
2513
normal zc
2544
normal zo
2544
normal zc
2686
normal zo
2686
normal zo
3378
normal zo
3379
normal zo
3404
normal zo
3404
normal zo
3404
normal zo
3404
normal zo
3404
normal zo
3404
normal zo
3404
normal zo
3404
normal zo
3404
normal zo
3416
normal zo
3417
normal zo
3417
normal zo
3441
normal zo
3417
normal zo
3417
normal zo
3416
normal zo
3379
normal zo
3378
normal zo
3623
normal zo
3630
normal zo
3642
normal zo
3642
normal zo
3642
normal zo
3642
normal zo
3642
normal zo
3652
normal zo
3652
normal zo
3652
normal zo
3630
normal zo
3623
normal zo
3781
normal zo
3789
normal zo
3800
normal zo
3800
normal zo
3800
normal zo
3800
normal zo
3800
normal zo
3810
normal zo
3810
normal zo
3810
normal zo
3789
normal zo
3781
normal zo
35
normal zo
let s:l = 477 - ((37 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
477
normal! 0
tabedit contractscont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
3argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
48
normal zo
97
normal zo
137
normal zo
137
normal zo
137
normal zo
137
normal zo
137
normal zo
137
normal zo
137
normal zo
137
normal zo
137
normal zo
144
normal zo
144
normal zo
144
normal zo
144
normal zo
144
normal zo
144
normal zo
144
normal zo
144
normal zo
144
normal zo
152
normal zo
152
normal zo
152
normal zo
152
normal zo
152
normal zo
97
normal zo
172
normal zo
212
normal zo
212
normal zo
212
normal zo
212
normal zo
212
normal zo
212
normal zo
212
normal zo
212
normal zo
212
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
172
normal zo
243
normal zo
264
normal zo
264
normal zc
281
normal zo
288
normal zo
289
normal zo
289
normal zo
289
normal zo
289
normal zo
289
normal zo
288
normal zo
281
normal zo
311
normal zo
318
normal zo
319
normal zo
319
normal zo
319
normal zo
319
normal zo
319
normal zo
318
normal zo
311
normal zo
342
normal zo
345
normal zo
345
normal zo
345
normal zo
349
normal zo
350
normal zo
350
normal zo
350
normal zo
350
normal zo
350
normal zo
349
normal zo
342
normal zo
373
normal zo
380
normal zo
381
normal zo
381
normal zo
381
normal zo
381
normal zo
381
normal zo
380
normal zo
373
normal zo
403
normal zo
410
normal zo
411
normal zo
411
normal zo
411
normal zo
411
normal zo
411
normal zo
410
normal zo
403
normal zo
243
normal zc
437
normal zo
439
normal zo
441
normal zo
442
normal zo
441
normal zo
444
normal zo
447
normal zo
447
normal zo
447
normal zo
451
normal zo
452
normal zo
452
normal zo
452
normal zo
455
normal zo
455
normal zo
455
normal zo
455
normal zo
455
normal zo
451
normal zo
444
normal zo
478
normal zo
481
normal zo
481
normal zo
481
normal zo
485
normal zo
486
normal zo
486
normal zo
486
normal zo
489
normal zo
489
normal zo
489
normal zo
489
normal zo
489
normal zo
485
normal zo
478
normal zo
513
normal zo
520
normal zo
520
normal zo
513
normal zo
548
normal zo
555
normal zo
555
normal zo
548
normal zo
583
normal zo
590
normal zo
590
normal zo
583
normal zo
437
normal zo
675
normal zo
772
normal zo
773
normal zo
774
normal zo
774
normal zo
774
normal zo
774
normal zo
774
normal zo
773
normal zo
772
normal zo
785
normal zo
786
normal zo
787
normal zo
787
normal zo
787
normal zo
787
normal zo
787
normal zo
786
normal zo
785
normal zo
798
normal zo
799
normal zo
800
normal zo
800
normal zo
800
normal zo
800
normal zo
800
normal zo
799
normal zo
798
normal zo
675
normal zo
816
normal zo
822
normal zo
822
normal zo
822
normal zo
825
normal zo
826
normal zo
826
normal zo
826
normal zo
826
normal zo
826
normal zo
825
normal zo
839
normal zo
840
normal zo
840
normal zo
840
normal zo
840
normal zo
840
normal zo
839
normal zo
816
normal zo
866
normal zo
870
normal zo
871
normal zo
873
normal zo
871
normal zo
870
normal zo
866
normal zo
901
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
912
normal zo
901
normal zo
1161
normal zo
1330
normal zo
1330
normal zo
1330
normal zo
1161
normal zo
1356
normal zo
1458
normal zo
1458
normal zo
1458
normal zo
1458
normal zo
1458
normal zo
1458
normal zo
1472
normal zo
1472
normal zo
1472
normal zo
1472
normal zo
1472
normal zo
1472
normal zo
1486
normal zo
1486
normal zo
1486
normal zo
1486
normal zo
1486
normal zo
1486
normal zo
1501
normal zo
1501
normal zo
1501
normal zo
1501
normal zo
1501
normal zo
1501
normal zo
1502
normal zo
1502
normal zo
1502
normal zo
1501
normal zo
1524
normal zo
1524
normal zo
1524
normal zo
1501
normal zo
1501
normal zo
1501
normal zo
1501
normal zo
1501
normal zo
1549
normal zo
1549
normal zo
1549
normal zo
1556
normal zo
1557
normal zo
1559
normal zo
1559
normal zo
1559
normal zo
1559
normal zo
1559
normal zo
1559
normal zo
1559
normal zo
1557
normal zo
1556
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1572
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zc
1713
normal zc
1713
normal zc
1713
normal zc
1713
normal zc
1356
normal zo
1735
normal zo
1741
normal zo
1741
normal zo
1741
normal zo
1744
normal zo
1745
normal zo
1745
normal zo
1745
normal zo
1745
normal zo
1745
normal zo
1744
normal zo
1757
normal zo
1759
normal zo
1760
normal zo
1760
normal zo
1760
normal zo
1760
normal zo
1760
normal zo
1759
normal zo
1757
normal zo
1776
normal zo
1777
normal zo
1777
normal zo
1777
normal zo
1777
normal zo
1776
normal zo
1735
normal zo
1904
normal zo
1924
normal zo
1926
normal zo
1927
normal zo
1927
normal zo
1927
normal zo
1927
normal zo
1927
normal zo
1926
normal zo
1924
normal zo
1904
normal zo
1974
normal zo
2002
normal zo
2002
normal zo
2002
normal zo
2002
normal zo
2002
normal zo
2002
normal zo
2002
normal zo
1974
normal zo
2219
normal zo
2219
normal zc
2243
normal zo
2243
normal zo
2301
normal zo
2301
normal zo
2366
normal zo
2367
normal zo
2368
normal zo
2370
normal zo
2368
normal zo
2367
normal zo
2379
normal zo
2380
normal zo
2381
normal zo
2381
normal zo
2393
normal zo
2394
normal zo
2394
normal zo
2393
normal zo
2400
normal zo
2400
normal zo
2380
normal zo
2379
normal zo
2407
normal zo
2407
normal zo
2407
normal zo
2407
normal zo
2407
normal zo
2414
normal zo
2415
normal zo
2416
normal zo
2416
normal zo
2416
normal zo
2415
normal zo
2421
normal zo
2426
normal zo
2426
normal zo
2430
normal zo
2430
normal zo
2434
normal zo
2434
normal zo
2434
normal zo
2434
normal zo
2434
normal zo
2414
normal zo
2454
normal zo
2455
normal zo
2455
normal zo
2455
normal zo
2455
normal zo
2455
normal zo
2454
normal zo
2459
normal zo
2459
normal zo
2459
normal zo
2459
normal zo
2459
normal zo
2464
normal zo
2465
normal zo
2465
normal zo
2465
normal zo
2465
normal zo
2465
normal zo
2464
normal zo
2471
normal zo
2471
normal zo
2471
normal zo
2471
normal zo
2471
normal zo
2366
normal zo
48
normal zo
let s:l = 1973 - ((51 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1973
normal! 08l
tabedit estimatingcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
7argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
37
normal zo
534
normal zo
535
normal zo
536
normal zo
541
normal zo
541
normal zo
541
normal zo
541
normal zo
542
normal zo
541
normal zo
541
normal zo
541
normal zo
541
normal zo
536
normal zo
535
normal zo
534
normal zo
617
normal zo
619
normal zo
619
normal zo
619
normal zo
619
normal zo
619
normal zo
619
normal zo
622
normal zo
622
normal zo
622
normal zo
622
normal zo
622
normal zo
622
normal zo
625
normal zo
625
normal zo
625
normal zo
625
normal zo
625
normal zo
625
normal zo
617
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
1082
normal zo
37
normal zo
let s:l = 546 - ((44 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
546
normal! 040l
tabedit labourcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
9argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
40
normal zo
4339
normal zo
4341
normal zo
4341
normal zo
4341
normal zo
4341
normal zo
4341
normal zo
4339
normal zo
6029
normal zo
6070
normal zo
6072
normal zo
6072
normal zo
6070
normal zo
6103
normal zo
6105
normal zo
6105
normal zc
6103
normal zc
6029
normal zc
6124
normal zo
6138
normal zo
6138
normal zo
6138
normal zo
6138
normal zo
6138
normal zo
6138
normal zo
6138
normal zo
6124
normal zo
6168
normal zo
6173
normal zo
6173
normal zo
6173
normal zo
6173
normal zo
6173
normal zo
6173
normal zo
6173
normal zo
6176
normal zo
6176
normal zo
6176
normal zo
6176
normal zo
6176
normal zo
6176
normal zo
6183
normal zo
6184
normal zo
6184
normal zo
6184
normal zo
6186
normal zo
6184
normal zo
6184
normal zo
6183
normal zo
6168
normal zo
6553
normal zo
6559
normal zo
6591
normal zo
6607
normal zo
6607
normal zo
6607
normal zc
6607
normal zo
6607
normal zo
6591
normal zc
6559
normal zo
6553
normal zo
6738
normal zo
6738
normal zc
6821
normal zo
6821
normal zc
6916
normal zo
6926
normal zo
6954
normal zo
6954
normal zo
6954
normal zo
6967
normal zo
6967
normal zo
6967
normal zc
6967
normal zo
6967
normal zo
6926
normal zc
6916
normal zc
6991
normal zo
7025
normal zo
7025
normal zo
7025
normal zo
7035
normal zo
7044
normal zo
7044
normal zo
7044
normal zo
7047
normal zo
7047
normal zo
7047
normal zo
7063
normal zo
7063
normal zo
7063
normal zo
7071
normal zo
7071
normal zo
7076
normal zo
7076
normal zo
7076
normal zo
7076
normal zo
7076
normal zo
7035
normal zo
7098
normal zo
7099
normal zo
7099
normal zo
7099
normal zo
7099
normal zo
7099
normal zo
7099
normal zo
7099
normal zo
7098
normal zo
7106
normal zo
7106
normal zo
7106
normal zo
6991
normal zc
7132
normal zo
7155
normal zo
7155
normal zo
7155
normal zo
7155
normal zo
7155
normal zo
7157
normal zo
7160
normal zo
7160
normal zo
7160
normal zo
7160
normal zo
7160
normal zo
7160
normal zo
7160
normal zo
7157
normal zc
7166
normal zo
7166
normal zo
7166
normal zo
7132
normal zo
7191
normal zo
7217
normal zo
7217
normal zo
7217
normal zo
7220
normal zo
7220
normal zo
7220
normal zo
7223
normal zo
7223
normal zo
7223
normal zo
7237
normal zo
7237
normal zo
7237
normal zo
7241
normal zo
7242
normal zo
7242
normal zo
7242
normal zo
7246
normal zo
7246
normal zo
7246
normal zo
7250
normal zo
7250
normal zo
7250
normal zo
7253
normal zo
7253
normal zo
7253
normal zo
7257
normal zo
7257
normal zo
7257
normal zo
7271
normal zo
7271
normal zo
7271
normal zo
7286
normal zo
7288
normal zo
7290
normal zo
7290
normal zo
7290
normal zo
7290
normal zo
7312
normal zo
7312
normal zo
7312
normal zo
7312
normal zo
7312
normal zo
7290
normal zo
7241
normal zo
7319
normal zo
7319
normal zo
7319
normal zo
7191
normal zo
7347
normal zo
7367
normal zo
7367
normal zo
7370
normal zo
7367
normal zo
7374
normal zo
7375
normal zo
7375
normal zo
7375
normal zo
7379
normal zo
7379
normal zo
7379
normal zo
7383
normal zo
7383
normal zo
7383
normal zo
7386
normal zo
7386
normal zo
7386
normal zo
7390
normal zo
7390
normal zo
7390
normal zo
7403
normal zo
7404
normal zo
7404
normal zo
7404
normal zo
7409
normal zo
7409
normal zc
7409
normal zo
7414
normal zo
7414
normal zo
7414
normal zo
7419
normal zo
7419
normal zo
7419
normal zo
7422
normal zo
7422
normal zo
7422
normal zo
7422
normal zc
7422
normal zo
7422
normal zo
7422
normal zo
7403
normal zo
7374
normal zo
7430
normal zo
7430
normal zc
7430
normal zo
7347
normal zc
7470
normal zo
7473
normal zo
7473
normal zo
7473
normal zo
7470
normal zo
40
normal zo
let s:l = 6175 - ((37 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
6175
normal! 0154l
tabedit productioncont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
14argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
51
normal zo
89
normal zo
154
normal zo
154
normal zo
154
normal zo
154
normal zo
154
normal zo
89
normal zo
573
normal zo
573
normal zo
666
normal zo
666
normal zo
759
normal zo
771
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
772
normal zo
771
normal zo
759
normal zo
1080
normal zo
1085
normal zo
1085
normal zo
1080
normal zo
1136
normal zo
1161
normal zo
1161
normal zo
1161
normal zo
1161
normal zo
1161
normal zo
1161
normal zo
1161
normal zo
1161
normal zo
1136
normal zo
1209
normal zo
1209
normal zo
1267
normal zo
1308
normal zo
1308
normal zo
1267
normal zo
1439
normal zo
1479
normal zo
1479
normal zo
1439
normal zc
1509
normal zo
1550
normal zo
1568
normal zo
1568
normal zo
1568
normal zo
1568
normal zo
1568
normal zo
1550
normal zo
1509
normal zc
1645
normal zo
1647
normal zo
1647
normal zo
1647
normal zo
1645
normal zo
1654
normal zo
1658
normal zo
1658
normal zo
1658
normal zo
1664
normal zo
1669
normal zo
1669
normal zo
1669
normal zo
1669
normal zo
1669
normal zo
1664
normal zo
1654
normal zo
1692
normal zo
1693
normal zo
1693
normal zc
1693
normal zo
1692
normal zc
1723
normal zc
1756
normal zo
1787
normal zo
1787
normal zo
1787
normal zo
1756
normal zc
1822
normal zo
1863
normal zo
1864
normal zo
1864
normal zo
1864
normal zo
1864
normal zo
1864
normal zo
1864
normal zo
1864
normal zo
1863
normal zo
1879
normal zo
1880
normal zo
1880
normal zo
1880
normal zo
1879
normal zo
1888
normal zo
1888
normal zo
1888
normal zo
1822
normal zc
1925
normal zo
1984
normal zo
1985
normal zo
1985
normal zo
1985
normal zo
1984
normal zo
1991
normal zo
1993
normal zo
1993
normal zc
1993
normal zo
1925
normal zo
2028
normal zo
2049
normal zo
2050
normal zo
2050
normal zo
2050
normal zo
2050
normal zo
2049
normal zo
2061
normal zo
2062
normal zo
2062
normal zo
2062
normal zo
2062
normal zo
2061
normal zo
2028
normal zc
2078
normal zo
2078
normal zo
2096
normal zo
2096
normal zo
2113
normal zo
2119
normal zo
2120
normal zo
2121
normal zo
2122
normal zo
2122
normal zo
2122
normal zo
2122
normal zo
2122
normal zo
2122
normal zo
2122
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2121
normal zo
2133
normal zo
2134
normal zo
2135
normal zo
2135
normal zo
2135
normal zo
2135
normal zo
2135
normal zo
2135
normal zo
2135
normal zo
2134
normal zo
2133
normal zo
2140
normal zo
2141
normal zo
2142
normal zo
2142
normal zo
2142
normal zo
2142
normal zo
2142
normal zo
2142
normal zo
2142
normal zo
2141
normal zo
2140
normal zo
2120
normal zo
2119
normal zc
2147
normal zo
2147
normal zo
2147
normal zo
2147
normal zo
2147
normal zo
2151
normal zo
2152
normal zo
2153
normal zo
2153
normal zo
2153
normal zo
2152
normal zo
2158
normal zo
2163
normal zo
2165
normal zo
2165
normal zo
2165
normal zo
2163
normal zo
2167
normal zo
2168
normal zo
2168
normal zo
2168
normal zo
2167
normal zo
2172
normal zo
2173
normal zo
2173
normal zo
2173
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2172
normal zo
2184
normal zo
2191
normal zo
2191
normal zo
2191
normal zo
2191
normal zo
2191
normal zo
2151
normal zo
2113
normal zo
2241
normal zo
2241
normal zo
2253
normal zo
51
normal zo
let s:l = 1922 - ((106 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1922
normal! 08l
tabedit est3yresshsfcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
4argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
43
normal zo
554
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
574
normal zo
554
normal zo
43
normal zo
let s:l = 31 - ((0 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 01l
tabedit est3yresspalisadecont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
5argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=1
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
46
normal zo
129
normal zo
129
normal zo
285
normal zo
285
normal zo
470
normal zo
475
normal zo
475
normal zo
475
normal zo
475
normal zo
475
normal zo
475
normal zo
470
normal zo
866
normal zo
866
normal zo
923
normal zo
936
normal zo
942
normal zo
942
normal zo
942
normal zo
942
normal zo
942
normal zo
942
normal zo
936
normal zo
923
normal zo
1198
normal zo
1198
normal zo
1260
normal zo
1260
normal zo
1353
normal zo
1364
normal zo
1364
normal zo
1364
normal zo
1364
normal zo
1364
normal zo
1364
normal zo
1353
normal zo
1411
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1415
normal zo
1411
normal zo
1602
normal zo
1602
normal zo
1808
normal zo
1808
normal zo
1827
normal zo
1828
normal zo
1828
normal zo
1828
normal zo
1839
normal zo
1839
normal zo
1842
normal zo
1842
normal zo
1842
normal zo
1839
normal zo
1827
normal zo
1975
normal zo
2022
normal zo
2026
normal zo
2026
normal zo
2026
normal zo
2027
normal zo
2026
normal zo
2026
normal zo
2026
normal zo
2022
normal zo
2033
normal zo
2033
normal zo
2033
normal zo
1975
normal zc
2286
normal zo
2289
normal zo
2289
normal zo
2289
normal zo
2291
normal zo
2289
normal zo
2289
normal zo
2289
normal zo
2286
normal zc
2504
normal zo
2511
normal zo
2511
normal zc
2511
normal zo
2538
normal zo
2538
normal zo
2538
normal zo
2578
normal zo
2579
normal zo
2579
normal zo
2579
normal zo
2587
normal zo
2587
normal zo
2578
normal zo
2504
normal zc
46
normal zo
let s:l = 30 - ((27 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
30
normal! 0
tabedit est5yreskomfencingcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
6argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
44
normal zo
284
normal zo
292
normal zo
292
normal zo
310
normal zo
311
normal zo
318
normal zo
311
normal zo
310
normal zo
284
normal zo
424
normal zo
424
normal zo
555
normal zo
555
normal zo
620
normal zo
634
normal zo
634
normal zo
634
normal zo
620
normal zo
44
normal zo
642
normal zo
let s:l = 641 - ((50 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
641
normal! 0
tabedit invoicingcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
8argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
35
normal zo
60
normal zo
60
normal zo
133
normal zo
136
normal zo
136
normal zo
150
normal zo
150
normal zo
157
normal zo
194
normal zo
198
normal zo
198
normal zo
198
normal zo
198
normal zo
198
normal zo
194
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
219
normal zo
229
normal zo
235
normal zo
235
normal zo
235
normal zo
235
normal zo
255
normal zo
255
normal zo
255
normal zo
235
normal zo
235
normal zo
235
normal zo
235
normal zo
229
normal zo
133
normal zo
268
normal zo
305
normal zo
311
normal zo
311
normal zo
311
normal zo
311
normal zo
311
normal zo
305
normal zo
268
normal zo
336
normal zo
396
normal zo
400
normal zo
400
normal zo
400
normal zo
400
normal zo
400
normal zo
396
normal zo
421
normal zo
421
normal zo
421
normal zo
421
normal zo
421
normal zo
431
normal zo
437
normal zo
437
normal zo
437
normal zo
437
normal zo
457
normal zo
457
normal zo
457
normal zo
437
normal zo
437
normal zo
437
normal zo
437
normal zo
431
normal zo
336
normal zo
472
normal zo
485
normal zo
485
normal zo
485
normal zo
489
normal zo
499
normal zo
499
normal zo
499
normal zo
499
normal zo
501
normal zo
501
normal zo
501
normal zo
499
normal zo
499
normal zo
499
normal zo
499
normal zo
489
normal zo
472
normal zo
573
normal zo
574
normal zo
575
normal zo
575
normal zo
575
normal zo
575
normal zo
575
normal zo
578
normal zo
578
normal zo
578
normal zo
578
normal zo
578
normal zo
574
normal zo
573
normal zo
648
normal zo
658
normal zo
658
normal zo
658
normal zc
658
normal zo
658
normal zo
664
normal zo
664
normal zo
664
normal zc
664
normal zo
664
normal zo
674
normal zo
675
normal zo
675
normal zo
675
normal zc
675
normal zo
675
normal zo
679
normal zo
680
normal zc
679
normal zc
674
normal zo
685
normal zo
691
normal zo
691
normal zo
691
normal zo
691
normal zo
691
normal zo
685
normal zo
648
normal zc
717
normal zo
717
normal zc
814
normal zo
814
normal zc
868
normal zo
868
normal zc
989
normal zo
989
normal zc
1112
normal zo
1112
normal zc
1161
normal zo
1161
normal zc
1303
normal zo
1303
normal zc
1371
normal zo
1371
normal zo
1422
normal zo
1425
normal zo
1426
normal zo
1432
normal zo
1426
normal zo
1425
normal zo
1439
normal zo
1440
normal zo
1442
normal zo
1440
normal zo
1439
normal zo
1447
normal zo
1422
normal zo
1626
normal zo
1626
normal zo
1894
normal zo
1894
normal zc
1965
normal zo
1965
normal zo
1977
normal zo
1977
normal zo
2031
normal zo
2031
normal zc
2042
normal zo
2043
normal zo
2046
normal zo
2046
normal zo
2046
normal zo
2046
normal zo
2046
normal zo
2049
normal zo
2049
normal zo
2049
normal zo
2049
normal zo
2049
normal zo
2043
normal zc
2042
normal zo
2118
normal zo
2119
normal zo
2123
normal zo
2123
normal zo
2123
normal zo
2123
normal zo
2123
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2126
normal zo
2131
normal zo
2131
normal zo
2131
normal zo
2131
normal zo
2131
normal zo
2144
normal zo
2144
normal zo
2144
normal zo
2144
normal zo
2144
normal zo
2144
normal zo
2144
normal zo
2144
normal zo
2144
normal zo
2119
normal zc
2118
normal zo
2194
normal zo
2195
normal zo
2201
normal zo
2201
normal zo
2195
normal zo
2194
normal zo
2295
normal zo
2296
normal zo
2297
normal zo
2297
normal zo
2297
normal zo
2296
normal zo
2295
normal zo
35
normal zo
let s:l = 1894 - ((10 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1894
normal! 0
tabedit managementcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
11argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
33
normal zo
42
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
54
normal zo
42
normal zc
61
normal zo
70
normal zo
75
normal zo
76
normal zo
77
normal zo
78
normal zo
78
normal zo
78
normal zo
78
normal zo
78
normal zo
78
normal zo
78
normal zo
77
normal zo
85
normal zo
86
normal zo
87
normal zo
87
normal zo
87
normal zo
87
normal zo
87
normal zo
87
normal zo
87
normal zo
86
normal zo
85
normal zo
76
normal zo
75
normal zo
91
normal zo
91
normal zo
91
normal zo
91
normal zo
91
normal zo
70
normal zc
96
normal zo
120
normal zo
123
normal zo
124
normal zo
124
normal zo
124
normal zo
124
normal zo
124
normal zo
123
normal zo
120
normal zo
146
normal zo
148
normal zo
149
normal zo
149
normal zo
149
normal zo
148
normal zo
146
normal zo
96
normal zc
209
normal zo
219
normal zo
220
normal zo
220
normal zo
220
normal zo
220
normal zo
220
normal zo
219
normal zo
225
normal zo
225
normal zo
225
normal zo
231
normal zo
233
normal zo
234
normal zo
234
normal zo
234
normal zo
234
normal zo
234
normal zo
233
normal zo
248
normal zo
248
normal zo
248
normal zo
248
normal zo
248
normal zo
231
normal zo
260
normal zo
260
normal zo
260
normal zo
260
normal zo
260
normal zo
260
normal zo
260
normal zo
209
normal zc
273
normal zo
276
normal zo
276
normal zc
276
normal zo
273
normal zc
311
normal zo
312
normal zc
311
normal zc
320
normal zo
320
normal zc
400
normal zo
401
normal zo
401
normal zc
447
normal zo
447
normal zo
447
normal zo
447
normal zo
447
normal zo
447
normal zo
447
normal zo
447
normal zo
400
normal zc
488
normal zo
494
normal zc
499
normal zc
510
normal zo
510
normal zc
530
normal zo
530
normal zo
530
normal zo
532
normal zo
532
normal zo
530
normal zo
530
normal zo
530
normal zo
613
normal zo
613
normal zo
613
normal zo
613
normal zo
613
normal zo
613
normal zo
613
normal zo
613
normal zo
613
normal zo
488
normal zc
621
normal zo
622
normal zo
622
normal zo
658
normal zo
660
normal zo
661
normal zo
661
normal zo
661
normal zo
661
normal zo
661
normal zo
660
normal zo
667
normal zo
667
normal zo
667
normal zo
658
normal zo
672
normal zo
673
normal zo
673
normal zo
675
normal zo
675
normal zo
675
normal zo
675
normal zo
675
normal zo
673
normal zo
673
normal zo
672
normal zo
621
normal zo
690
normal zo
691
normal zo
694
normal zc
691
normal zo
690
normal zc
823
normal zo
825
normal zo
827
normal zo
829
normal zo
831
normal zo
833
normal zo
835
normal zo
837
normal zo
839
normal zo
847
normal zo
849
normal zo
850
normal zo
851
normal zo
851
normal zo
851
normal zo
851
normal zo
851
normal zo
851
normal zo
851
normal zo
850
normal zo
855
normal zo
856
normal zo
856
normal zo
856
normal zo
856
normal zo
856
normal zo
856
normal zo
856
normal zo
855
normal zo
849
normal zo
847
normal zo
865
normal zo
893
normal zo
897
normal zo
897
normal zo
897
normal zo
897
normal zo
897
normal zo
893
normal zo
865
normal zc
966
normal zo
971
normal zo
972
normal zo
973
normal zo
973
normal zo
981
normal zo
982
normal zo
982
normal zo
981
normal zo
972
normal zo
971
normal zo
987
normal zo
987
normal zo
987
normal zo
987
normal zo
987
normal zo
966
normal zc
993
normal zo
1047
normal zo
1051
normal zo
1051
normal zo
1051
normal zo
1051
normal zo
1051
normal zo
1047
normal zo
1087
normal zo
1087
normal zo
993
normal zc
1139
normal zo
1139
normal zc
1496
normal zo
1534
normal zo
1535
normal zo
1535
normal zo
1535
normal zo
1535
normal zo
1535
normal zo
1535
normal zo
1535
normal zo
1535
normal zo
1535
normal zo
1534
normal zo
1565
normal zo
1565
normal zo
1565
normal zo
1565
normal zo
1565
normal zo
1565
normal zo
1565
normal zo
1565
normal zo
1627
normal zo
1627
normal zo
1627
normal zo
1627
normal zo
1627
normal zo
1627
normal zo
1627
normal zo
1627
normal zo
1496
normal zo
1686
normal zo
1690
normal zo
1690
normal zo
1690
normal zo
1698
normal zo
1720
normal zo
1720
normal zo
1720
normal zo
1734
normal zo
1734
normal zo
1734
normal zo
1734
normal zo
1734
normal zo
1698
normal zo
1766
normal zo
1769
normal zo
1769
normal zo
1769
normal zo
1769
normal zo
1769
normal zo
1769
normal zo
1769
normal zo
1766
normal zo
1686
normal zo
1851
normal zo
1851
normal zc
1959
normal zo
1960
normal zo
1960
normal zo
1960
normal zo
1959
normal zc
2063
normal zo
2071
normal zo
2076
normal zo
2076
normal zo
2092
normal zo
2092
normal zc
2092
normal zo
2102
normal zo
2102
normal zc
2102
normal zo
2112
normal zo
2116
normal zo
2116
normal zo
2124
normal zo
2146
normal zo
2146
normal zo
2146
normal zo
2153
normal zc
2171
normal zo
2175
normal zo
2171
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2178
normal zo
2112
normal zo
2063
normal zo
2206
normal zo
2213
normal zo
2214
normal zo
2213
normal zo
2219
normal zo
2219
normal zo
2219
normal zo
2229
normal zo
2229
normal zo
2229
normal zo
2239
normal zo
2239
normal zo
2239
normal zo
2249
normal zo
2253
normal zo
2253
normal zo
2283
normal zo
2283
normal zo
2283
normal zo
2308
normal zo
2308
normal zo
2316
normal zo
2316
normal zo
2316
normal zo
2316
normal zo
2316
normal zo
2249
normal zo
2206
normal zo
2344
normal zo
2436
normal zo
2436
normal zo
2436
normal zo
2436
normal zo
2436
normal zo
2436
normal zo
2436
normal zo
2344
normal zc
2449
normal zo
2457
normal zo
2458
normal zo
2459
normal zo
2460
normal zo
2460
normal zo
2460
normal zo
2460
normal zo
2460
normal zo
2460
normal zo
2460
normal zo
2459
normal zo
2467
normal zo
2468
normal zo
2469
normal zo
2469
normal zo
2469
normal zo
2469
normal zo
2469
normal zo
2469
normal zo
2469
normal zo
2468
normal zo
2467
normal zc
2458
normal zc
2457
normal zo
2519
normal zo
2519
normal zo
2519
normal zo
2519
normal zo
2519
normal zo
2519
normal zo
2519
normal zo
2449
normal zc
33
normal zo
let s:l = 669 - ((41 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
669
normal! 0106l
tabedit manufacturecont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
12argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=1
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
34
normal zo
119
normal zo
120
normal zo
120
normal zo
122
normal zo
122
normal zo
120
normal zo
120
normal zo
128
normal zo
129
normal zo
129
normal zo
129
normal zo
129
normal zo
129
normal zo
129
normal zo
129
normal zo
128
normal zo
119
normal zo
385
normal zo
386
normal zo
386
normal zo
387
normal zo
387
normal zo
386
normal zo
386
normal zo
385
normal zo
411
normal zo
415
normal zo
416
normal zo
416
normal zo
416
normal zo
416
normal zo
417
normal zo
416
normal zo
416
normal zo
416
normal zo
415
normal zo
411
normal zo
437
normal zo
446
normal zo
449
normal zo
449
normal zo
449
normal zo
449
normal zo
449
normal zo
449
normal zo
449
normal zo
446
normal zo
437
normal zo
476
normal zo
478
normal zo
476
normal zo
484
normal zo
498
normal zo
515
normal zo
484
normal zo
536
normal zo
558
normal zo
560
normal zo
566
normal zo
567
normal zo
567
normal zo
567
normal zo
567
normal zo
567
normal zo
566
normal zo
573
normal zo
576
normal zo
576
normal zo
576
normal zo
576
normal zc
576
normal zo
576
normal zo
576
normal zo
573
normal zc
590
normal zo
590
normal zo
590
normal zo
536
normal zc
616
normal zo
616
normal zc
717
normal zo
717
normal zc
749
normal zo
768
normal zo
769
normal zo
773
normal zo
779
normal zo
784
normal zo
784
normal zo
784
normal zo
784
normal zo
784
normal zo
784
normal zo
784
normal zo
784
normal zo
784
normal zo
779
normal zo
790
normal zo
790
normal zo
790
normal zo
792
normal zo
793
normal zo
792
normal zo
790
normal zo
799
normal zo
799
normal zo
799
normal zo
790
normal zo
790
normal zo
768
normal zo
749
normal zc
839
normal zo
844
normal zo
844
normal zo
858
normal zo
859
normal zo
860
normal zo
859
normal zo
858
normal zo
869
normal zo
869
normal zo
869
normal zo
839
normal zc
904
normal zo
904
normal zc
943
normal zo
945
normal zo
945
normal zo
946
normal zo
947
normal zo
948
normal zc
947
normal zc
946
normal zc
945
normal zo
945
normal zo
943
normal zo
976
normal zo
978
normal zo
981
normal zo
981
normal zo
982
normal zo
983
normal zo
984
normal zo
983
normal zo
982
normal zo
981
normal zo
981
normal zo
976
normal zo
996
normal zo
1026
normal zo
1031
normal zo
1026
normal zo
1038
normal zo
1050
normal zo
1038
normal zo
34
normal zo
1121
normal zo
1122
normal zo
1124
normal zo
1121
normal zo
let s:l = 1117 - ((75 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1117
normal! 0
tabedit logisticscont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
edit logisticscont.py
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
38
normal zo
68
normal zo
503
normal zo
550
normal zo
550
normal zo
550
normal zo
550
normal zo
550
normal zo
557
normal zo
557
normal zo
557
normal zo
557
normal zo
557
normal zo
579
normal zo
583
normal zo
583
normal zo
583
normal zo
583
normal zo
583
normal zo
588
normal zo
588
normal zo
588
normal zo
588
normal zo
588
normal zo
579
normal zo
603
normal zo
603
normal zo
603
normal zo
603
normal zo
603
normal zo
609
normal zo
611
normal zo
611
normal zo
611
normal zo
611
normal zo
623
normal zo
623
normal zo
623
normal zo
611
normal zo
611
normal zo
611
normal zo
611
normal zo
609
normal zo
503
normal zc
632
normal zo
632
normal zo
649
normal zo
649
normal zc
690
normal zo
690
normal zc
918
normal zo
1016
normal zo
1016
normal zo
918
normal zo
1052
normal zc
1074
normal zo
1074
normal zc
1094
normal zo
1094
normal zc
1145
normal zo
1145
normal zo
1200
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1205
normal zo
1200
normal zo
1239
normal zo
1249
normal zo
1249
normal zo
1249
normal zo
1249
normal zo
1249
normal zo
1239
normal zo
1262
normal zc
1431
normal zo
1451
normal zo
1451
normal zo
1451
normal zo
1451
normal zo
1451
normal zo
1468
normal zo
1507
normal zo
1507
normal zo
1507
normal zo
1507
normal zo
1507
normal zo
1517
normal zo
1517
normal zo
1517
normal zo
1531
normal zo
1531
normal zo
1531
normal zo
1507
normal zo
1507
normal zo
1507
normal zo
1507
normal zo
1507
normal zo
1468
normal zo
1431
normal zo
1546
normal zo
1547
normal zo
1551
normal zo
1546
normal zo
1578
normal zo
1579
normal zo
1579
normal zo
1579
normal zo
1579
normal zo
1579
normal zo
1578
normal zo
1603
normal zo
1604
normal zo
1604
normal zo
1604
normal zo
1604
normal zo
1604
normal zo
1612
normal zo
1603
normal zo
1627
normal zo
1640
normal zo
1640
normal zo
1640
normal zo
1640
normal zo
1640
normal zo
1644
normal zo
1644
normal zo
1644
normal zo
1644
normal zo
1644
normal zo
1649
normal zo
1649
normal zo
1649
normal zo
1649
normal zo
1649
normal zo
1656
normal zo
1656
normal zo
1656
normal zo
1656
normal zo
1656
normal zo
1675
normal zo
1686
normal zo
1689
normal zo
1691
normal zo
1686
normal zo
1694
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1713
normal zo
1675
normal zo
1627
normal zo
1754
normal zo
1801
normal zo
1807
normal zo
1816
normal zo
1819
normal zo
1821
normal zo
1816
normal zo
1824
normal zo
1830
normal zo
1830
normal zo
1830
normal zo
1830
normal zo
1830
normal zo
1830
normal zo
1830
normal zo
1830
normal zo
1830
normal zo
1807
normal zo
1801
normal zo
1754
normal zo
1871
normal zo
1880
normal zo
1880
normal zo
1880
normal zo
1880
normal zo
1880
normal zo
1902
normal zo
1922
normal zo
1923
normal zo
1923
normal zo
1923
normal zo
1923
normal zo
1923
normal zo
1923
normal zo
1923
normal zo
1923
normal zo
1923
normal zo
1922
normal zo
1902
normal zo
1871
normal zo
1956
normal zo
1989
normal zo
2012
normal zo
2013
normal zo
2013
normal zo
2013
normal zo
2013
normal zo
2013
normal zo
2013
normal zo
2013
normal zo
2013
normal zo
2013
normal zo
2012
normal zo
1989
normal zo
1956
normal zo
2055
normal zo
2067
normal zo
2067
normal zo
2069
normal zo
2067
normal zo
2067
normal zo
2055
normal zo
2164
normal zo
2198
normal zo
2200
normal zo
2200
normal zo
2200
normal zo
2226
normal zo
2200
normal zo
2200
normal zo
2200
normal zo
2198
normal zo
2164
normal zo
2356
normal zo
2383
normal zo
2392
normal zo
2392
normal zo
2392
normal zo
2392
normal zo
2392
normal zo
2383
normal zo
2356
normal zo
2551
normal zo
2586
normal zo
2587
normal zo
2590
normal zo
2590
normal zo
2590
normal zo
2590
normal zo
2590
normal zo
2596
normal zo
2597
normal zo
2597
normal zo
2597
normal zo
2597
normal zo
2597
normal zo
2597
normal zo
2596
normal zo
2601
normal zo
2601
normal zo
2601
normal zo
2601
normal zo
2601
normal zo
2587
normal zo
2606
normal zo
2607
normal zo
2607
normal zo
2607
normal zo
2607
normal zo
2607
normal zo
2618
normal zo
2618
normal zo
2618
normal zo
2618
normal zo
2618
normal zo
2606
normal zo
2624
normal zo
2625
normal zo
2625
normal zo
2625
normal zo
2625
normal zo
2624
normal zo
2586
normal zo
2551
normal zo
2765
normal zo
2800
normal zo
2802
normal zo
2802
normal zo
2802
normal zo
2802
normal zo
2802
normal zo
2802
normal zo
2802
normal zo
2802
normal zo
2800
normal zo
2765
normal zo
2822
normal zo
2859
normal zo
2861
normal zo
2861
normal zo
2861
normal zo
2861
normal zo
2861
normal zo
2861
normal zo
2861
normal zo
2861
normal zo
2859
normal zo
2822
normal zo
2888
normal zo
2919
normal zo
2930
normal zo
2932
normal zo
2932
normal zo
2932
normal zo
2932
normal zo
2932
normal zo
2932
normal zo
2930
normal zo
2919
normal zo
2888
normal zo
2949
normal zo
2957
normal zo
2957
normal zo
2957
normal zo
2957
normal zo
2957
normal zo
2957
normal zo
2957
normal zo
2957
normal zo
2974
normal zo
2975
normal zo
2975
normal zo
2975
normal zo
2975
normal zo
2975
normal zo
2975
normal zo
2975
normal zo
2978
normal zo
2978
normal zo
2978
normal zo
3002
normal zo
3003
normal zo
3003
normal zo
3003
normal zo
3007
normal zo
3007
normal zo
3007
normal zo
3028
normal zo
3028
normal zo
3028
normal zo
3028
normal zo
3029
normal zo
3029
normal zo
3029
normal zo
3029
normal zo
3029
normal zo
3029
normal zo
3028
normal zo
3028
normal zo
3028
normal zo
3028
normal zo
3002
normal zo
2974
normal zo
3076
normal zo
3076
normal zo
3076
normal zo
3076
normal zo
3076
normal zo
3076
normal zo
3076
normal zo
2949
normal zo
3085
normal zo
3136
normal zo
3138
normal zo
3138
normal zo
3138
normal zo
3138
normal zo
3138
normal zo
3138
normal zo
3138
normal zo
3138
normal zo
3136
normal zo
3085
normal zo
3273
normal zo
3321
normal zo
3345
normal zo
3345
normal zo
3345
normal zo
3345
normal zo
3346
normal zo
3346
normal zo
3346
normal zo
3346
normal zo
3346
normal zo
3346
normal zo
3345
normal zo
3345
normal zo
3345
normal zo
3345
normal zo
3321
normal zo
3273
normal zo
3398
normal zo
3406
normal zo
3406
normal zo
3406
normal zo
3409
normal zo
3410
normal zo
3410
normal zo
3411
normal zo
3411
normal zo
3411
normal zo
3411
normal zo
3411
normal zo
3415
normal zo
3415
normal zo
3415
normal zo
3415
normal zo
3415
normal zo
3415
normal zo
3410
normal zo
3410
normal zo
3409
normal zo
3430
normal zo
3430
normal zo
3430
normal zo
3430
normal zo
3431
normal zo
3431
normal zo
3431
normal zo
3431
normal zo
3431
normal zo
3430
normal zo
3430
normal zo
3430
normal zo
3430
normal zo
3461
normal zo
3461
normal zo
3461
normal zo
3461
normal zo
3462
normal zo
3462
normal zo
3462
normal zo
3462
normal zo
3462
normal zo
3462
normal zo
3461
normal zo
3461
normal zo
3461
normal zo
3461
normal zo
3545
normal zo
3546
normal zo
3546
normal zo
3546
normal zo
3546
normal zo
3547
normal zo
3547
normal zo
3547
normal zo
3547
normal zo
3547
normal zo
3547
normal zo
3546
normal zo
3546
normal zo
3546
normal zo
3546
normal zo
3545
normal zo
3398
normal zo
3611
normal zo
3630
normal zo
3635
normal zo
3636
normal zo
3636
normal zo
3636
normal zo
3636
normal zo
3637
normal zo
3637
normal zo
3637
normal zo
3637
normal zo
3637
normal zo
3637
normal zo
3636
normal zo
3636
normal zo
3636
normal zo
3636
normal zo
3635
normal zo
3630
normal zo
3611
normal zo
3723
normal zo
3734
normal zo
3735
normal zo
3735
normal zo
3741
normal zo
3741
normal zo
3735
normal zo
3735
normal zo
3734
normal zo
3780
normal zo
3804
normal zo
3804
normal zo
3804
normal zo
3804
normal zo
3805
normal zo
3805
normal zo
3805
normal zo
3805
normal zo
3847
normal zo
3847
normal zo
3847
normal zo
3805
normal zo
3805
normal zo
3804
normal zo
3804
normal zo
3804
normal zo
3804
normal zo
3780
normal zo
3723
normal zo
4004
normal zo
4004
normal zo
4056
normal zo
4056
normal zo
4293
normal zo
4293
normal zo
4404
normal zo
4426
normal zo
4430
normal zo
4442
normal zo
4442
normal zo
4442
normal zo
4442
normal zo
4442
normal zo
4430
normal zo
4426
normal zo
4404
normal zo
38
normal zo
let s:l = 2629 - ((47 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2629
normal! 041l
tabedit marketingcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
13argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
29
normal zo
29
normal zo
let s:l = 155 - ((0 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
155
normal! 04l
tabedit receptioncont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
15argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
32
normal zo
48
normal zo
56
normal zo
57
normal zo
77
normal zo
78
normal zo
79
normal zo
79
normal zo
79
normal zo
79
normal zo
79
normal zo
79
normal zo
79
normal zo
78
normal zo
77
normal zo
57
normal zo
56
normal zo
88
normal zo
88
normal zo
88
normal zo
88
normal zo
88
normal zo
48
normal zo
158
normal zo
158
normal zo
283
normal zo
320
normal zo
323
normal zo
323
normal zc
320
normal zc
283
normal zo
32
normal zo
let s:l = 306 - ((0 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
306
normal! 016l
tabedit transportcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
17argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
29
normal zo
54
normal zo
61
normal zo
61
normal zo
61
normal zo
83
normal zo
83
normal zo
83
normal zo
83
normal zo
83
normal zo
54
normal zo
96
normal zo
96
normal zo
113
normal zo
113
normal zo
218
normal zo
226
normal zo
227
normal zo
227
normal zo
227
normal zo
227
normal zo
227
normal zo
226
normal zo
244
normal zo
244
normal zo
244
normal zo
251
normal zo
259
normal zo
259
normal zo
259
normal zo
259
normal zo
259
normal zo
262
normal zo
262
normal zo
262
normal zo
266
normal zo
266
normal zo
266
normal zo
266
normal zo
266
normal zo
266
normal zo
266
normal zo
218
normal zo
275
normal zo
278
normal zo
278
normal zo
278
normal zo
283
normal zo
287
normal zo
288
normal zo
288
normal zo
288
normal zo
292
normal zo
292
normal zo
292
normal zo
292
normal zo
292
normal zo
287
normal zo
275
normal zo
318
normal zo
328
normal zo
333
normal zo
333
normal zo
333
normal zo
333
normal zo
333
normal zo
328
normal zo
318
normal zo
380
normal zo
388
normal zo
402
normal zo
402
normal zo
402
normal zo
402
normal zo
402
normal zo
388
normal zo
430
normal zo
430
normal zo
430
normal zo
430
normal zo
430
normal zo
430
normal zo
430
normal zo
380
normal zo
540
normal zo
540
normal zo
600
normal zo
600
normal zo
670
normal zo
670
normal zo
731
normal zo
732
normal zo
732
normal zo
732
normal zo
752
normal zo
752
normal zo
770
normal zo
771
normal zo
772
normal zo
771
normal zo
770
normal zo
779
normal zo
780
normal zo
781
normal zo
781
normal zo
781
normal zo
781
normal zo
781
normal zo
780
normal zo
785
normal zo
786
normal zo
786
normal zo
786
normal zo
786
normal zo
786
normal zo
785
normal zo
779
normal zc
792
normal zo
792
normal zo
794
normal zo
792
normal zo
792
normal zo
731
normal zc
909
normal zo
910
normal zo
910
normal zo
910
normal zo
913
normal zo
913
normal zo
914
normal zo
915
normal zo
916
normal zo
915
normal zo
914
normal zo
913
normal zo
913
normal zo
909
normal zo
955
normal zo
973
normal zo
973
normal zo
973
normal zo
979
normal zo
994
normal zo
994
normal zo
994
normal zo
994
normal zo
994
normal zo
979
normal zo
1016
normal zo
1017
normal zo
1017
normal zo
1017
normal zo
1017
normal zo
1017
normal zo
1017
normal zo
1017
normal zo
1016
normal zo
955
normal zc
1059
normal zo
1059
normal zo
1167
normal zo
1167
normal zo
1277
normal zo
1277
normal zo
1514
normal zo
1545
normal zo
1514
normal zo
1671
normal zo
1671
normal zo
1853
normal zo
1853
normal zo
29
normal zo
let s:l = 251 - ((31 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
251
normal! 026l
tabedit fleetcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
edit fleetcont.py
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
27
normal zo
39
normal zo
45
normal zo
65
normal zo
72
normal zo
72
normal zo
72
normal zo
72
normal zo
72
normal zo
65
normal zc
156
normal zo
156
normal zo
197
normal zo
197
normal zo
379
normal zo
379
normal zo
748
normal zo
749
normal zo
749
normal zc
748
normal zc
800
normal zo
810
normal zo
810
normal zo
843
normal zo
845
normal zc
810
normal zc
864
normal zo
865
normal zo
866
normal zo
866
normal zo
866
normal zo
866
normal zo
866
normal zo
865
normal zo
871
normal zo
872
normal zo
872
normal zo
872
normal zo
872
normal zo
872
normal zo
871
normal zo
864
normal zo
876
normal zo
876
normal zo
876
normal zo
876
normal zo
881
normal zo
882
normal zo
882
normal zo
882
normal zo
882
normal zo
881
normal zo
886
normal zo
887
normal zo
887
normal zo
887
normal zo
887
normal zo
886
normal zo
892
normal zo
892
normal zo
892
normal zo
800
normal zc
902
normal zo
902
normal zc
953
normal zo
954
normal zo
954
normal zc
985
normal zo
985
normal zo
985
normal zo
985
normal zo
990
normal zo
991
normal zo
991
normal zo
991
normal zo
991
normal zo
990
normal zo
995
normal zo
996
normal zo
996
normal zo
996
normal zo
996
normal zo
995
normal zo
1001
normal zo
1001
normal zo
1001
normal zo
953
normal zc
1011
normal zo
1015
normal zo
1015
normal zo
1015
normal zo
1019
normal zo
1019
normal zo
1019
normal zo
1023
normal zc
1026
normal zo
1027
normal zo
1028
normal zo
1028
normal zo
1028
normal zo
1031
normal zo
1031
normal zo
1031
normal zo
1031
normal zo
1031
normal zo
1027
normal zo
1026
normal zo
1042
normal zo
1011
normal zc
1048
normal zo
1052
normal zo
1052
normal zo
1052
normal zo
1056
normal zo
1057
normal zo
1057
normal zo
1057
normal zo
1060
normal zo
1060
normal zo
1060
normal zo
1063
normal zo
1063
normal zo
1063
normal zo
1063
normal zo
1063
normal zo
1056
normal zo
1074
normal zo
1048
normal zc
1080
normal zo
1083
normal zo
1083
normal zo
1083
normal zo
1080
normal zc
1093
normal zo
1096
normal zo
1096
normal zo
1096
normal zo
1093
normal zc
1102
normal zo
1103
normal zo
1103
normal zo
1103
normal zo
1103
normal zo
1103
normal zo
1106
normal zo
1107
normal zo
1107
normal zo
1108
normal zo
1107
normal zo
1107
normal zo
1106
normal zo
1112
normal zo
1114
normal zc
1112
normal zc
1102
normal zo
27
normal zo
1121
normal zo
1122
normal zo
1121
normal zo
let s:l = 197 - ((29 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
197
normal! 030l
tabedit vettingcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
18argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 5 - ((0 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5
normal! 0
tabedit cctvcont.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
2argu
let s:cpo_save=&cpo
set cpo&vim
iabbr <buffer> iff if object: <Left>
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:XCOMM,n:>,fb:-
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal concealcursor=
setlocal conceallevel=0
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
set foldlevel=4
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
set foldmethod=indent
setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=2
setlocal imsearch=2
setlocal include=^\\s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255
setlocal keywordprg=pydoc
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal nomodeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=175
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
49
normal zo
49
normal zo
49
normal zo
49
normal zo
49
normal zo
49
normal zo
49
normal zo
49
normal zo
49
normal zo
63
normal zo
63
normal zo
63
normal zo
63
normal zo
63
normal zo
78
normal zo
93
normal zo
97
normal zo
97
normal zo
97
normal zo
97
normal zo
97
normal zo
93
normal zo
132
normal zo
151
normal zo
151
normal zo
151
normal zo
151
normal zo
151
normal zo
132
normal zo
158
normal zo
167
normal zo
174
normal zo
174
normal zo
174
normal zo
174
normal zo
174
normal zo
174
normal zo
174
normal zo
167
normal zo
177
normal zo
177
normal zo
177
normal zo
177
normal zo
177
normal zo
158
normal zo
184
normal zo
78
normal zo
let s:l = 159 - ((24 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
159
normal! 036l
tabnext 4
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
