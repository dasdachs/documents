MAIN = element:(variable / word ) { return element; }

/** Variables **/
start = ws "{{" ws
end = ws "}}" ws

variable = start name:var_char* end { return {"name": name.join("")}; }

word = ws chars:char* ws { return [chars.join("")]; }

/** Characters and constatns **/

// TODO: DRY!!
var_char "valid_variable_characters" = c:[^\0-\x20] { return c; }

char "valid_characters" = c:[^\0-\x1F] {return c; }

ws "whitespace" = [ \t\r\n]* // ws = machine readable "whitespace" human readable
