# Lists in ObjectScript

This topic provides an overview of the ObjectScript native list format and alternatives. One simple alternative is the delimited string. There are class-based alternatives as well.

## Native List Format

ObjectScript provides a native list format. This format is sometimes called $LIST format, because the $LIST function is used to work with these lists.

The only supported way to work with the native list format is to use the ObjectScript list functions. The internal structure of this kind of list is not documented and is subject to change without notice.

In class definitions, if you want a property to use the native list format, declare the property type as %Library.List or the short name %List.

## List Functions

The ObjectScript native list format consists of an encoded list of substrings, known as elements. These lists can only be handled using the following list functions:

*   List creation:
    
    *   $LISTBUILD creates a list by specifying each element as a parameter value.
        
    *   $LISTFROMSTRING creates a list by specifying a string that contains delimiters. The function uses the delimiter to divide the string into elements.
        
    *   $LIST creates a list by extracting it as a sublist from an existing list.
        
*   List data retrieval:
    
    *   $LIST returns a list element value by position. It can count positions from the beginning or the end of the list.
        
    *   $LISTNEXT returns list element values sequentially from the beginning of the list. While both `$LIST` and `$LISTNEXT` can be used to sequentially return elements from a list, `$LISTNEXT` is significantly faster when returning a large number of list elements.
        
    *   $LISTGET returns a list element value by position, or returns a default value.
        
    *   $LISTTOSTRING returns all of the element values in a list as a delimited string.
        
*   List manipulation:
    
    *   SET $LIST inserts, updates, or deletes elements in a list. `SET $LIST` replaces a list element or a range of list elements with one or more values. Because `SET $LIST` can replace a list element with more than one element, you can use it to insert elements into a list. Because `SET $LIST` can replace a list element with a null string, you can use it to delete a list element or a range of list elements.
        
*   List evaluation:
    
    *   $LISTVALID determines if a string is a valid list.
        
    *   $LISTLENGTH determines the number of elements in a list.
        
    *   $LISTDATA determines if a specified list element contains data.
        
    *   $LISTFIND determines if a specified value is found in a list, returning the list position.
        
    *   $LISTSAME determines if two lists are identical.
        

Because a list is an encoded string, InterSystems IRIS treats lists slightly differently than standard strings. Therefore, you should not use standard string functions on lists. Further, using most list functions on a standard string generates a <LIST> error.

The following procedure demonstrates the use of the various list functions:

```objectscript
ListTest() PUBLIC {
    // set values for list elements
    SET Addr="One Memorial Drive"
    SET City="Cambridge"
    SET State="MA"
    SET Zip="02142"

    // create list
    SET Mail = $LISTBUILD(Addr,City,State,Zip)

    // get user input
    READ "Enter a string: ",input,!,!

    // if user input is part of the list, print the list's content
    IF $LISTFIND(Mail,input) {
        FOR i=1:1:$LISTLENGTH(Mail) {
            WRITE $LIST(Mail,i),!
        }
     }
}
```

This procedure demonstrates several notable aspects of lists:

*   `$LISTFIND` only returns 1 (True) if the value being tested matches the list item exactly.
    
*   `$LISTFIND` and `$LISTLENGTH` are used in expressions.
    

For more detailed information on list functions see the corresponding reference pages in the ObjectScript Reference.

## Sparse Lists and Sublists

A function that adds an element value to a list by position will add enough list elements to place the value in the proper position. For example:

```objectscript
  SET $LIST(Alphalist,1)="a"
  SET $LIST(Alphalist,20)="t"
  WRITE $LISTLENGTH(Alphalist)
```

Because the second `$LIST` in this example creates list element 20, `$LISTLENGTH` returns a value of 20. However, elements 2 through 19 do not have values set. Hence, if you attempt to display any of their values, you will receive a <NULL VALUE> error. You can use `$LISTGET` to avoid this error.

An element in a list can itself be a list. To retrieve a value from a sublist such as this, nest `$LIST` function calls, as in the following code:

```objectscript
  SET $LIST(Powers,2)=$LISTBUILD(2,4,8,16,32)
  WRITE $LIST($LIST(Powers,2),5)
```

This code returns 32, which is the value of the fifth element in the sublist contained by the second element in the `Powers` list. (In the `Powers` list, the second item is a sublist of two raised to the first through fifth powers, so that the first item in the sublist is two to the first power, and so on.)

## List Compression

The ListFormat setting controls whether Unicode strings should be compressed when stored in a $LIST encoded string. By default, only $DOUBLE values are compressed. Compressed format is automatically handled by InterSystems IRIS. Do not pass compressed lists to external clients, such as Java or C#, without verifying that they support the compressed format.

The per-process behavior can be controlled using the ListFormat() method of the %SYSTEM.Process class.

The system-wide default behavior can be established by setting the ListFormat property of the Config.Miscellaneous class or the InterSystems IRIS Management Portal, as follows: from `System Administration`, select `Configuration`, `Additional Settings`, `Compatibility`.

## Delimited Strings as an Alternative

As a simple alternative to the native list format, you can use a delimiter-separated string as a list. In this case, you generally use the following functions:

*   `$PIECE` — Returns a specific piece of a string based on a specified delimiter. It can also return a range of pieces, as well as multiple pieces from a single string, based on multiple delimiters.
    
*   `$LENGTH` — Returns the number of pieces in a string based on a specified delimiter.
    

The `$PIECE` function provides uniquely important functionality because it allows you to use a single string that contains multiple substrings, with a special delimiter character (such as `^`) to separate them. The large string acts as a record, and the substrings are its fields.

The syntax for `$PIECE` is:

```objectscript
 WRITE $PIECE("ListString","QuotedDelimiter",ItemNumber)
```

where `ListString` is a quoted string that contains the full record being used; `QuotedDelimiter` is the specified delimited, which must appear in quotes; and `ItemNumber` is the specified substring to be returned. For example, to display the second item in the following space-delimited list, the syntax is:

```objectscript
 WRITE $PIECE("Kennedy Johnson Nixon"," ",2)
```

which returns `Johnson`.

You can also return multiple members of the list, so that the following:

```objectscript
 WRITE $PIECE("Nixon***Ford***Carter***Reagan","***",1,3)
```

returns `Nixon***Ford***Carter`. Note that both values must refer to actual substrings and the third argument (here 1) must be a smaller value than that of the fourth argument (here 3).

The delimiter can be anything you choose, such as with the following list:

```objectscript
 SET x = $PIECE("Reagan,Bush,Clinton,Bush,Obama",",",3)
 SET y = $PIECE("Reagan,Bush,Clinton,Bush,Obama","Bush",2)
 WRITE x,!,y
```

which returns

```
Clinton
,Clinton,
```

In the first case, the delimiter is the comma; in the second, it is the string `Bush`, which is why the returned string includes the commas. To avoid any possible ambiguities related to delimiters, use the list-related functions, described in the next section.

### Advanced $PIECE Features

A call to `$PIECE` that sets the value of a delimited element in a list will add enough list items so that it can place the substring as the proper item in an otherwise empty list. For instance, suppose some code sets the first, then the fourth, then the twentieth item in a list,

```objectscript
 SET $PIECE(Alphalist, "^", 1) = "a"
 WRITE "First, the length of the list is ",$LENGTH(Alphalist,"^"),".",!
 SET $PIECE(Alphalist, "^", 4) = "d"
 WRITE "Then, the length of the list is ",$LENGTH(Alphalist,"^"),".",!
 SET $PIECE(Alphalist, "^", 20) = "t"
 WRITE "Finally, the length of the list is ",$LENGTH(Alphalist,"^"),".",!
```

The `$LENGTH` function returns a value of 1, then 4, then 20, since it creates the necessary number of delimited items. However, items 2, 3, and 5 through 19 do not have values set. Hence, if you attempt to display any of their values, nothing appears.

A delimited string item can also contain a delimited string. To retrieve a value from a sublist such as this, nest `$PIECE` function calls, as in the following code:

```objectscript
 SET $PIECE(Powers, "^", 1) = "1::1::1::1::1"
 SET $PIECE(Powers, "^", 2) = "2::4::8::16::32"
 SET $PIECE(Powers, "^", 3) = "3::9::27::81::243"
 WRITE Powers,!
 WRITE $PIECE( $PIECE(Powers, "^", 2), "::", 3)
```

This code returns two lines of output: the first is the string `Powers`, including all its delimiters; the second is 8, which is the value of the third element in the sublist contained by the second element in `Powers`. (In the `Powers` list, the `n`th item is a sublist of two raised to the first through fifth powers, so that the first item in the sublist is `n` to the first power, and so on.)

For more details, see $PIECE.

## Lists and Delimited Strings Compared

The native list format provides the following advantages, when compared to delimited strings:

*   The native list format does not require a designated delimiter. Though the `$PIECE` function allows you to manage a string containing multiple data items, it depends on setting aside a character (or character string) as a dedicated delimiter. When using delimiters, there is always the chance that one of the data items will contain the delimiter character(s) as data, which will throw off the positions of the pieces in the delimited string. A list is useful for avoiding delimiters altogether, and thus allowing any character or combination of characters to be entered as data.
    
*   Data elements can be retrieved faster from a list (using `$LIST` or `$LISTNEXT`) than from a delimited string (using `$PIECE`). For sequential data retrieval, `$LISTNEXT` is significantly faster than `$LIST`, and both are significantly faster than `$PIECE`.
    

A delimited string provides different advantages, when compared to the native list format:

*   A delimited string allows you to more flexibly search the contents of data, using the `$FIND` function. Because `$LISTFIND` requires an exact match, you cannot search for partial substrings in lists. Hence, in the example above, using `$LISTFIND` to search for the string `One` in the Mail list return 0 (indicating failure), even though the address `One Memorial Drive` begins with the characters `One`.
    
*   Because a delimited string is a standard string, you can use all of the standard string functions on it. Because a native list is an encoded string, you can only use $List functions on it.
    

## Class-Based Lists

Rather than the native list format or delimited strings, you can use list classes that use different structure and that provide an object-based API. InterSystems IRIS provides a set of classes you can use as list-form class properties, and another set of classes you can use for standalone lists.

## See Also

*   Working with Collection Classes
