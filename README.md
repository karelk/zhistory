# zhistory

add following function to .zshrc:

```sh
h () {
	if [ "$#" -eq 0 ]
	then
		local LINES="$((`tput lines` - 2))" 
		history -t '(%a) %Y-%b-%d %H:%M' 0 | tail -n "$LINES" | /usr/local/bin/zhistory.py '$'
	else
		history -t '(%a) %Y-%b-%d %H:%M' 0 | /usr/local/bin/zhistory.py $@
	fi
}
```

and search throuh zsh history using grep-like options:

```
 -A NUM
    print NUM lines after matching line

 -B NUM
    print NUM lines before matching line

 -C NUM
    print NUM lines of context

 -F, --fixed-strings
    interpret PATTERN as literal string

 -i, --ignorecase
    ignore case

 -t, --time
    match time

 -w, --word
    match whole words
```


