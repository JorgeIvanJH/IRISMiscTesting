# Working with Globals

This page describes the various operations you can perform using multidimensional storage (globals).

> **Note:**
> 
> When using direct global access within applications, develop and adhere to a naming convention to keep different parts of an application from “walking over” one another; this is similar to developing naming convention for classes, method, and other variables. Also, avoid certain global names that InterSystems IRIS data platform uses; for a list of these, see Global Variable Names to Avoid.

## Storing Data in Globals

Storing data in global nodes is simple: you treat a global as you would any other variable. The difference is that operations on globals are automatically written to the database.

### Creating Globals

There is no setup work required to create a new global; simply setting data into a global implicitly creates a new global structure. You can create a global (or a global subscript) and place data in it with a single operation, or you can create a global (or subscript) and leave it empty by setting it to the null string. In ObjectScript, these operations are done using the `SET` command.

The following examples define a global named `Color` (if one does not already exist) and associate the value “Red” with it. If a global already exists with the name `Color`, then these examples modify it to contain the new information.

In ObjectScript:

```objectscript
 SET ^Color = "Red"
```

### Storing Data in Global Nodes

To store a value within a global subscript node, simply set the value of the global node as you would any other variable. If the specified node did not previously exist, it is created. If it did exist, its contents are replaced with the new value.

You can store any data in a global node, with the exception that any global node cannot contain a string longer than the string length limit, which is extremely long. See General System Limits.

Setting the value of a global node is an atomic operation: It is guaranteed to succeed and you do not need to use any locks to ensure concurrency.

```objectscript
   SET ^TEST = 2
   SET ^TEST("Color")="Red"
   SET ^TEST(1,1)=100        /* The 2nd-level subscript (1,1) is set
                                to the value 100. No value is stored at
                                the 1st-level subscript (^TEST(1)). */
   SET ^TEST(^TEST)=10       /* The value of global variable ^TEST
                                is the name of the subscript. */
   SET ^TEST(a,b)=50         /* The values of local variables a and b
                                are the names of the subscripts. */
   SET ^TEST(a+10)=50
```

Also, you can construct global references at runtime using indirection.

## Deleting Global Nodes

To remove a global node, a group of subnodes, or an entire global from the database, use the ObjectScript `KILL` or `ZKILL` commands.

The `KILL` command deletes all nodes (data as well as its corresponding entry in the array) at a specific global reference, including any descendant subnodes. That is, all nodes starting with the specified subscript are deleted.

For example, the ObjectScript statement:

```objectscript
  KILL ^TEST
```

deletes the entire ^TEST global. A subsequent reference to this global would return an <UNDEFINED> error.

The ObjectScript statement:

```objectscript
   KILL ^TEST(100)
```

deletes contents of node 100 within the ^TEST global. If there are descendant subnodes, such as ^TEST(100,1), ^TEST(100,2), and ^TEST(100,1,2,3), these are deleted as well.

The ObjectScript `ZKILL` command deletes a specified global or global subscript node. It does not delete descendant subnodes.

> **Note:**
> 
> Following the kill of a large global, the space once occupied by that global may not have been completely freed, since the blocks are marked free in the background by the Garbage Collector daemon. Thus, a call to the `ReturnUnusedSpace` method of the SYS.Database class immediately after killing a large global may not return as much space as expected, since blocks occupied by that global may not have been released as yet.

You cannot use the `NEW` command on global variables.

## Testing the Existence of a Global Node

To test if a specific global (or its descendants) contains data, use the `$DATA` function.

`$DATA` returns a value indicating whether or not the specified global reference exists. The possible return values are:

<table><tr><th>Status Value</th><th>Meaning</th></tr><tr><td>0</td><td>The global variable is undefined.</td></tr><tr><td>1</td><td>The global variable exists and contains data, but has no descendants. Note that the null string ("") qualifies as data.</td></tr><tr><td>10</td><td>The global variable has descendants (contains a downward pointer to a subnode) but does not itself contain data. Any direct reference to such a variable will result in an &lt;UNDEFINED&gt; error. For example, if $DATA(^y) returns 10, SET x=^y will produce an &lt;UNDEFINED&gt; error.</td></tr><tr><td>11</td><td>The global variable both contains data and has descendants (contains a downward pointer to a subnode).</td></tr></table>

## Retrieving the Value of a Global Node

To get the value stored within a specific global node, simply use the global reference as an expression:

```objectscript
   SET color = ^TEST("Color")    ; assign to a local variable
   WRITE ^TEST("Color")          ; use as a command argument
   SET x=$LENGTH(^TEST("Color")) ; use as a function parameter
```

### The $GET Function

You can also get the value of a global node using the `$GET` function:

```objectscript
   SET mydata = $GET(^TEST("Color"))
```

This retrieves the value of the specified node (if it exists) or returns the null string ("") if the node has no value. You can use the optional second argument of `$GET` to return a specified default value if the node has no value.

### The WRITE, ZWRITE, and ZZDUMP Commands

You can display the contents of a global or a global subnode by using the various ObjectScript display commands. The `WRITE` command returns the value of the specified global or subnode as a string. The `ZWRITE` command returns the name of the global variable and its value, and each of its descendant nodes and their values. The `ZZDUMP` command returns the value of the specified global or subnode in hexadecimal dump format.

## Traversing Data within a Global

There are a number of ways to traverse (iterate over) data stored within a global.

### The $ORDER (Next / Previous) Function

The ObjectScript `$ORDER` function allows you to sequentially visit each node within a global.

Given a subscript (or set of subscripts) as an argument, the `$ORDER` function returns the value of the next subscript at a given level. This is best explained by example. Suppose you have defined a set of nodes in a global named `^TEST`, as follows:

```objectscript
 Set ^TEST(1) = ""
 Set ^TEST(1,1) = ""
 Set ^TEST(1,2) = ""
 Set ^TEST(2) = ""
 Set ^TEST(2,1) = ""
 Set ^TEST(2,2) = ""
 Set ^TEST(5,1,2) = ""
```

To find the first, first-level subscript, we can use:

```objectscript
 SET key = $ORDER(^TEST(""))
```

This returns the first, top-level subscript following the null string (""). (The null string is used to represent the subscript value before the first entry; as a return value it is used to indicate that there are no following subscript values.) In this example, `key` will now contain the value 1.

We can find the next, top-level subscript by using 1 or `key` in the `$ORDER` expression:

```objectscript
 SET key = $ORDER(^TEST(key))
```

If `key` has an initial value of 1, then this statement will set it to 2 (because ^TEST(2) is the next first-level subscript). Executing this statement again will set `key` to 5 as that is the next first-level subscript. Note that 5 is returned even though there is no data stored directly at ^TEST(5). Executing this statement one more time will set `key` to the null string (""), indicating that there are no more first level subscripts.

By using additional subscripts with the `$ORDER` function, you can iterate over different subscript levels. For example, using the data above, the statement:

```objectscript
 SET key = $ORDER(^TEST(1,""))
```

will set `key` to 1 because ^TEST(1,1) is the next second-level subscript. Executing this statement again will set `key` to 2 as that is the next second-level subscript. Executing this statement one more time will set `key` to `""` indicating that there are no more second-level subscripts under node ^TEST(1).

#### Looping with $ORDER

The following ObjectScript code defines a simple global and then loops over all of its first-level subscripts:

```objectscript
 // clear ^TEST in case it has data
 Kill ^TEST

 // fill in ^TEST with sample data
 For i = 1:1:100 {
     // Set each node to a random person's name
     Set ^TEST(i) = ##class(%PopulateUtils).Name()
 }

 // loop over every node
 // Find first node
 Set key = $Order(^TEST(""))

 While (key '= "") {
     // Write out contents
     Write "#", key, " ", ^TEST(key),!

     // Find next node
     Set key = $Order(^TEST(key))
 }
```

#### Additional $ORDER Arguments

The ObjectScript `$ORDER` function takes optional second and third arguments. The second argument is a direction flag indicating in which direction you wish to traverse a global. The default, 1, specifies forward traversal, while –1 specifies backward traversal.

The third argument, if present, contains a local variable name. If the node found by `$ORDER` contains data, the data found is written into this local variable. When you are looping over a global and you are interested in node values as well as subscript values, this approach is efficient and requires the fewest coding steps.

### Looping Over a Global

If you know that a given global is organized using contiguous numeric subscripts, you can use a simple For loop to iterate over its values. For example:

```objectscript
 For i = 1:1:100 {
     Write ^TEST(i),!
 }
```

Generally, it is better to use the `$ORDER` function described above: it is more efficient and you do not have to worry about gaps in the data (such as a deleted node).

### The $QUERY Function

If you need to visit every node and subnode within a global, moving up and down over subnodes, use the ObjectScript `$QUERY` function. (Alternatively you can use nested `$ORDER` loops).

The `$QUERY` function takes a global reference and returns a string containing the global reference of the next node in the global (or "" if there are no following nodes). To use the value returned by `$QUERY`, you must use the ObjectScript indirection operator (@).

For example, suppose you define the following global:

```objectscript
 Set ^TEST(1) = ""
 Set ^TEST(1,1) = ""
 Set ^TEST(1,2) = ""
 Set ^TEST(2) = ""
 Set ^TEST(2,1) = ""
 Set ^TEST(2,2) = ""
 Set ^TEST(5,1,2) = ""
```

The following call to `$QUERY`:

```objectscript
 SET node = $QUERY(^TEST(""))
```

sets `node` to the string “^TEST(1)”, the address of the first node within the global. Then, to get the next node in the global, call `$QUERY` again and use the indirection operator on `node`:

```objectscript
 SET node = $QUERY(@node)
```

At this point, `node` contains the string “^TEST(1,1)”.

The following example defines a set of global nodes and then walks over them using `$QUERY`, writing the address of each node as it does:

```objectscript
 Kill ^TEST // make sure ^TEST is empty

 // place some data into ^TEST
 Set ^TEST(1) = ""
 Set ^TEST(1,1) = ""
 Set ^TEST(1,2) = ""
 Set ^TEST(2) = ""
 Set ^TEST(2,1) = ""
 Set ^TEST(2,2) = ""
 Set ^TEST(5,1,2) = ""

 // now walk over ^TEST
 // find first node
 Set node = $Query(^TEST(""))
 While (node '= "") {
     Write node,!
     // get next node
     Set node = $Query(@node)
 }
```

## Copying Data within Globals

To copy the contents of a global (entire or partial) into another global (or a local array), use the ObjectScript `MERGE` command.

The following example demonstrates the use of the `MERGE` command to copy the entire contents of the `^OldData` global into the `^NewData` global:

```objectscript
 Merge ^NewData = ^OldData
```

If the source argument of the `MERGE` command has subscripts then all data in that node and its descendants are copied. If the destination argument has subscripts, then the data is copied using the destination address as the top level node. For example, the following code:

```objectscript
 Merge ^NewData(1,2) = ^OldData(5,6,7)
```

copies all the data at and beneath `^OldData(5,6,7)` into `^NewData(1,2)`.

## Maintaining Shared Counters within Globals

A major concurrency bottleneck of large-scale transaction processing applications can be the creation of unique identifier values. For example, consider an order processing application in which each new invoice must be given a unique identifying number. The traditional approach is to maintain some sort of counter table. Every process creating a new invoice waits to acquire a lock on this counter, increments its value, and unlocks it. This can lead to heavy resource contention over this single record.

To deal with this issue, InterSystems IRIS provides the ObjectScript `$INCREMENT` function. `$INCREMENT` atomically increments the value of a global node (if the node has no value, it is set to 1). The atomic nature of `$INCREMENT` means that no locks are required; the function is guaranteed to return a new incremented value with no interference from any other process.

You can use `$INCREMENT` as follows. First, you must decide upon a global node in which to hold the counter. Next, whenever you need a new counter value, simply invoke `$INCREMENT`:

```objectscript
 SET counter = $INCREMENT(^MyCounter)
```

For persistent classes (other than those created via SQL, the default storage structure uses `$INCREMENT` to assign unique object (row) identifier values. For persistent classes created via SQL, the default storage structure instead uses $SEQUENCE.

## Sorting Data within Globals

Data stored within globals is automatically sorted according to the value of the subscripts. For example, the following ObjectScript code defines a set of globals (in random order) and then iterates over them to demonstrate that the global nodes are automatically sorted by subscript:

```objectscript
 // Erase any existing data
 Kill ^TEST

 // Define a set of global nodes
 Set ^TEST("Cambridge") = ""
 Set ^TEST("New York") = ""
 Set ^TEST("Boston") = ""
 Set ^TEST("London") = ""
 Set ^TEST("Athens") = ""

 // Now iterate and display (in order)
 Set key = $Order(^TEST(""))
 While (key '= "") {
     Write key,!
     Set key = $Order(^TEST(key)) // next subscript
 }
```

Applications can take advantage of the automatic sorting provided by globals to perform sort operations or to maintain ordered, cross-referenced indexes on certain values. InterSystems SQL and ObjectScript use globals to perform such tasks automatically.

### Collation of Global Nodes

The order in which the nodes of a global are sorted (referred to as collation) is controlled at two levels: within the global itself and by the application using the global.

At the application level, you can control how global nodes are collated by performing data transformations on the values used as subscripts (InterSystems SQL and objects do this via user-specified collation functions). For example, if you wish to create a list of names that is sorted alphabetically but ignores case, then typically you use the uppercase version of the name as a subscript:

```objectscript
 // Erase any existing data
 Kill ^TEST

 // Define a set of global nodes for sorting
 For name = "Cobra","jackal","zebra","AARDVark" {
     // use UPPERCASE name as subscript
     Set ^TEST($ZCONVERT(name,"U")) = name
 }

 // Now iterate and display (in order)
 Set key = $Order(^TEST(""))
 While (key '= "") {
     Write ^TEST(key),!  // write untransformed name
     Set key = $Order(^TEST(key)) // next subscript
 }
```

This example converts each name to uppercase (using the $ZCONVERT function) so that the subscripts are sorted without regard to case. Each node contains the untransformed value so that the original value can be displayed.

### Numeric and String-Valued Subscripts

Numeric values are collated before string values; that is a value of 1 comes before a value of “a”. You need to be aware of this fact if you use both numeric and string values for a given subscript. If you are using a global for an index (that is, to sort data based on values), it is most common to either sort values as numbers (such as salaries) or strings (such as postal codes).

For numerically collated nodes, the typical solution is to coerce subscript values to numeric values using the unary `+` operator. For example, if you are building an index that sort `id` values by `age`, you can coerce `age` to always be numeric:

```objectscript
 Set ^TEST(+age,id) = ""
```

If you wish to sort values as strings (such as “0022”, “0342”, “1584”) then you can coerce the subscript values to always be strings by prepending a space (“ ”) character. For example, if you are building an index that sort `id` values by `zipcode`, you can coerce `zipcode` to always be a string:

```objectscript
 Set ^TEST(" "_zipcode,id) = ""
```

This ensures that values with leading zeroes, such as “0022” are always treated as strings.

### The $SORTBEGIN and $SORTEND Functions

Typically you do not have to worry about sorting data within InterSystems IRIS. Whether you use SQL or direct global access, sorting is handled automatically.

There are, however, certain cases where sorting can be done more efficiently. Specifically, in cases where (1) you need to set a large number of global nodes that are in random (that is, unsorted) order and (2) the total size of the resulting global approaches a significant portion of the InterSystems IRIS buffer pool, then performance can be adversely affected — since many of the `SET` operations involve disk operations (as data does not fit in the cache). This scenario usually arises in cases involving the creation of index globals such as bulk data loads, index population, or sorting of unindexed values in temporary globals.

To handle these cases efficiently, ObjectScript provides the `$SORTBEGIN` and `$SORTEND` functions. The `$SORTBEGIN` function initiates a special mode for a global (or part thereof) in which data set into the global is written to a special scratch buffer and sorted in memory (or temporary disk storage). When the `$SORTEND` function is called at the end of the operation, the data is written to actual global storage sequentially. The overall operation is much more efficient as the actual writing is done in an order requiring far fewer disk operations.

The `$SORTBEGIN` function is quite easy to use; simply invoke it with the name of the global you wish to sort before beginning the sort operation and call `$SORTEND` when the operation is complete:

```objectscript
 // Erase any existing data
 Kill ^TEST

 // Initiate sort mode for ^TEST global
 Set ret = $SortBegin(^TEST)

 // Write random data into ^TEST
 For i = 1:1:10000 {
     Set ^TEST($Random(1000000)) = ""
 }

 Set ret = $SortEnd(^TEST)

 // ^TEST is now set and sorted

 // Now iterate and display (in order)
 Set key = $Order(^TEST(""))
 While (key '= "") {
     Write key,!
     Set key = $Order(^TEST(key)) // next subscript
 }
```

The `$SORTBEGIN` function is designed for the special case of global creation and must be used with some care. Specifically, you must not read from the global to which you are writing while in `$SORTBEGIN` mode; as the data is not written, reads will be incorrect.

InterSystems SQL automatically uses these functions for creation of temporary index globals (such as for sorting on unindexed fields).

## Using Indirection with Globals

By means of indirection, ObjectScript provides a way to create global references at runtime. This can be useful in applications where you do not know global structure or names at program compilation time.

Indirection is supported via the indirection operator, `@`, which de-references a string containing an expression. There are several types of indirection, based on how the `@` operator is used.

The following code provides an example of name indirection in which the `@` operator is used to de-reference a string containing a global reference:

```objectscript
 // Erase any existing data
 Kill ^TEST

 // Set var to an global reference expression
 Set var = "^TEST(100)"

 // Now use indirection to set ^TEST(100)
 Set @var = "This data was set indirectly."

 // Now display the value directly:
 Write "Value: ",^TEST(100)
```

You can also use subscript indirection to mix expressions (variables or literal values) within indirect statements:

```objectscript
 // Erase any existing data
 Kill ^TEST

 // Set var to a subscript value
 Set glvn = "^TEST"

 // Now use indirection to set ^TEST(1) to ^TEST(10)
 For i = 1:1:10 {
     Set @glvn@(i) = "This data was set indirectly."
 }

 // Now display the values directly:
 Set key = $Order(^TEST(""))
 While (key '= "") {
     Write "Value ",key, ": ", ^TEST(key),!
     Set key = $Order(^TEST(key))
 }
```

Indirection is a fundamental feature of ObjectScript; it is not limited to global references. For more information, see Indirection. Indirection is less efficient than direct access, so you should use it judiciously.

## Managing Concurrency

The operation of setting or retrieving a single global node is atomic; it is guaranteed to always succeed with consistent results. For operations on multiple nodes, InterSystems IRIS provides the ability to acquire and release locks. See Locking and Concurrency Control.

## Checking the Most Recent Global Reference

The most recent global reference is recorded in the ObjectScript `$ZREFERENCE` special variable. `$ZREFERENCE` contains the most recent global reference, including subscripts and extended global reference, if specified. Note that `$ZREFERENCE` indicates neither whether the global reference succeeded, nor if the specified global exists. InterSystems IRIS simply records the most recently specified global reference.

### Naked Global Reference

Following a subscripted global reference, InterSystems IRIS sets a naked indicator to that global name and subscript level. You can then make subsequent references to the same global and subscript level using a naked global reference, omitting the global name and higher level subscripts. This streamlines repeated references to the same global at the same (or lower) subscript level.

Specifying a lower subscript level in a naked reference resets the naked indicator to that subscript level. Therefore, when using naked global references, you are always working at the subscript level established by the most recent global reference.

The naked indicator value is recorded in the `$ZREFERENCE` special variable. The naked indicator is initialized to the null string. Attempting a naked global reference when the naked indicator is not set results in a <NAKED> error. Changing namespaces reinitializes the naked indicator. You can reinitialize the naked indicator by setting `$ZREFERENCE` to the null string ("").

In the following example, the subscripted global ^Produce(“fruit”,1) is specified in the first reference. InterSystems IRIS saves this global name and subscript in the naked indicator, so that the subsequent naked global references can omit the global name “Produce” and the higher subscript level “fruit”. When the ^(3,1) naked reference goes to a lower subscript level, this new subscript level becomes the assumption for any subsequent naked global references.

```objectscript
   SET ^Produce("fruit",1)="Apples"  /* Full global reference  */
   SET ^(2)="Oranges"                /* Naked global references */
   SET ^(3)="Pears"                  /* assume subscript level 2 */
   SET ^(3,1)="Bartlett pears"       /* Go to subscript level 3  */
   SET ^(2)="Anjou pears"            /* Assume subscript level 3 */
   WRITE "latest global reference is: ",$ZREFERENCE,!
   ZWRITE ^Produce
   KILL ^Produce
```

This example sets the following global variables: ^Produce("fruit",1), ^Produce("fruit",2), ^Produce("fruit",3), ^Produce("fruit",3,1), and ^Produce("fruit",3,2).

With few exceptions, every global reference (full or naked) sets the naked indicator. The `$ZREFERENCE` special variable contains the full global name and subscripts of the most recent global reference, even if this was a naked global reference. The `ZWRITE` command also displays the full global name and subscripts of each global, whether or not it was set using a naked reference.

Naked global references should be used with caution, because InterSystems IRIS sets the naked indicator in situations that are not always obvious, including the following:

*   A full global reference initially sets the naked indicator, and subsequent full global references or naked global references change the naked indicator, even when the global reference is not successful. For example attempting to `WRITE` the value of a nonexistent global sets the naked indicator.
    
*   A command postconditional that references a subscripted global sets the naked indicator, regardless of how InterSystems IRIS evaluates the postconditional.
    
*   An optional function argument that references a subscripted global may or may not set the naked indicator, depending on whether InterSystems IRIS evaluates all arguments. For example the second argument of `$GET` always sets the naked indicator, even when the default value it contains is not used. InterSystems IRIS evaluates arguments in left-to-right sequence, so the last argument may reset the naked indicator set by the first argument.
    
*   The `TROLLBACK` command, which rolls back a transaction, does not roll back the naked indicator to its value at the beginning of the transaction.
    

If a full global reference contains an extended global reference, subsequent naked global references assume the same extended global reference; you do not have to specify the extended reference as part of a naked global reference.

## See Also

*   Introduction to Globals
    
*   Temporary Globals and the IRISTEMP Database
