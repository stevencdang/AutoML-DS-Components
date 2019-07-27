set nocompatible
filetype off

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" " alternatively, pass a path where Vundle should install plugins
" "call vundle#begin('~/some/path/here')
"
" " let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
"
" " The following are examples of different formats supported.
" " Keep Plugin commands between vundle#begin/end.
" " plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
" " plugin from http://vim-scripts.org/vim/scripts.html
Plugin 'L9'
Plugin 'ctrlpvim/ctrlp.vim'
" " git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" " The sparkup vim script is in a subdirectory of this repo called vim.
" " Pass the path to set the runtimepath properly.
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}

"""""" My Plugins
" " NERDTree Plugin
Plugin 'scrooloose/nerdtree'
" " NERDCommenter Plugin
Plugin 'scrooloose/nerdcommenter'
" " Vim-css3 Plugin
Plugin 'hail2u/vim-css3-syntax'
" " Vim Python Debugger
Plugin 'gotcha/vimpdb'
" " Vim Less highlighting
Bundle 'genoma/vim-less'
" " Vim command and communication with screen/tmux
Plugin 'ervandew/screen'
" " Vim R connection to send lines of code to and instance or R
" Plugin 'jalvesaq/Nvim-R'
" " Python Mode plugin for pylint, rope pydoc, pyflakes, pep8 etc
" " Bundle 'klen/python-mode'
" " vim-jedi plugin for python autocompletion
" Bundle 'davidhalter/jedi-vim'
" " TagbarToggle plugin for viewing class definitions in file
" Plugin 'majutsushi/tagbar'
" " Toggling line nubers from absolute to relative
Bundle 'myusuf3/numbers.vim'
" " Vim Ipython integration
Plugin 'wilywampa/vim-ipython'
" " Python PEP8 indentation
Plugin 'hattya/python-indent.vim'
" " Vim typescript syntax highlighting
Plugin 'leafgarland/typescript-vim'

 
" " All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" " To ignore plugin indent changes, instead use:
" ' filetype plugin on
" "
" " Brief help
" " :PluginList       - lists configured plugins
" " :PluginInstall    - installs plugins; append `!` to update or just
" :PluginUpdate
" " :PluginSearch foo - searches for foo; append `!` to refresh local cache
" " :PluginClean      - confirms removal of unused plugins; append `!` to
" auto-approve removal
" "
" see :h vundle for more details or wiki for FAQ
" " Put your non-Plugin stuff after this line

" " Custom key mapping shortcuts
" " Set leader key to spacebar
let mapleader = " "
set showcmd
" nmap <F8> : TagbarToggle<CR>
" " Initiate Jupyter/Ipython server connection
nmap <F10> :IPython<CR>

nmap gy : tabp<CR>
nmap gn :NERDTreeToggle<CR>
nmap tl :set nonumber<CR>
nmap tk :set number<CR>
" " Toggle 'paste' mode by pressing F3 for pasting text into vim
set pastetoggle=<F3>
nmap <F4> :NumbersToggle<CR>
nmap <F5> :NumbersOnOff<CR>
" " Screen.vim shortcuts
nmap <F1> :ScreenShell
" " Vim Quickfix shortcuts
nmap gf :cnext<CR>
nmap gb :cprev<CR>
nmap gl :clist<CR>

nmap <silent> <A-Up> :wincmd k<CR>
nmap <silent> <A-Down> :wincmd j<CR>
nmap <silent> <A-Left> :wincmd h<CR>
nmap <silent> <A-Right> :wincmd l<CR>
nmap <silent> <leader>- :resize -5<CR>
nmap <silent> <leader>= :resize +5<CR>"


" " execute pathogen#infect()
" " autocmd vimenter * NERDTree
"
" " Python pymode plugin config
" let g:pymode_options = 1
" let g:pymode_trim_whitespaces = 1
" let g:pymode_options_max_line_length = 119 
" let g:pymode_indent = 1
" let g:pymode_folding = 1
" let g:pymode_run = 1
" let g:pymode_run_bind = '<leader>r'
" let g:pymode_lint=1
" let g:pymode_link_checker= "pyflakes, pep8"
" let g:pymode_lint_on_write = 1
" let g:pymode_lint_on_fly = 0
" let g:pymode_doc = 1
" let g:pymode_doc_key = 'K'
" let g:pymode_rope = 0
" let g:pymode_rope_completion = 0
" let g:pymode_rope_complete_on_dot = 0
" let g:pymode_rope_organize_imports_bind = '<C-c>ro'
" let g:pymode_syntax = 1
" let g:pymode_syntax_all = 1
" let g:pymode_syntax_indent_errors = g:pymode_syntax_all
" let g:ropevim_vim_completion=0

" " Vim-Jedi Python autocompletion settings
" let g:jedi#auto_initialization = 1
" let g:jedi#use_splits_not_buffers = "right"
" let g:jedi#show_call_signatures = "2"
" let g:jedi#popup_on_dot = 0

" Vim-R config Settings
" " Start an R instance/connection
" nmap <F6> :<Plug>RStart<CR>
" send selection to R with space bar
" vmap <Space> :<Plug>RDSendSelection<CR>
" " send line to R with space bar
" nmap <Space> :<Plug>RDSendLine<CR>
let R_path = '/usr/bin'
"
filetype indent on
" set smartindent
set autoindent
set number
set expandtab
set tabstop=2
set shiftwidth=2
set colorcolumn=80

" Typescript settings
setlocal indentkeys+=0.

set foldmethod=indent
set nofoldenable
set foldlevel=1

filetype plugin on
set nocompatible
set t_Co=256
set background=dark
" colorscheme jellybeans
" colorscheme desert
colorscheme distinguished
" colorscheme guardian
syntax on
set backspace=indent,eol,start

" " IMPORTANT: grep will sometimes skip displaying the file name if you
" " search in a singe file. This will confuse Latex-Suite. Set your grep
" " program to always generate a file-name.
set grepprg=grep\ -nH\ $*

