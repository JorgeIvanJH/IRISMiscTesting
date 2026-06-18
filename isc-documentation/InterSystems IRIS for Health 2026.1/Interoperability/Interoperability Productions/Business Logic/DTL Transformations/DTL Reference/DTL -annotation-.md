# DTL <annotation>

Provides a descriptive comment for a DTL element, within a DTL transformation.

## Syntax

```
<annotation>
   <![CDATA[ Sends patient data from lab to CRM system. ]]>
</annotation>
```

## Description

The <annotation> element allows you to associate a descriptive comment with a DTL element. An <annotation> must appear as the first child of the element that it is annotating. For example:

```xml
<transform targetClass='Demo.DTL.ExampleTarget'
           sourceClass='Demo.DTL.ExampleSource'
           create='new'
           language='objectscript'>
  <annotation>
    <![CDATA[Implement current naming conventions.]]>
  </annotation>
  <trace value='"Convert from lowercase to uppercase"'/>
  <assign property='target.UpperCase'
          value='$ZCONVERT(source.LowerCase,"U")'
          action='set'>
   <annotation>This is a comment for the assign element</annotation>
  </assign>
</transform>
```

The previous example uses CDATA syntax around the annotation text. This convention is optional, but it lets you use line breaks and special characters such as the apostrophe (') without worrying about XML escape sequences. The maximum length of the <annotation> string is 32,767 characters, including the CDATA escape characters.

Also notice that the annotation for the assign element appears as a child immediately following the opening assign tag.

Most elements within DTL support <annotation> as a child element. This allows you to associate a descriptive comment with a DTL element. Unlike BPL, which offers positional attributes for every element, <annotation> is the only child element or attribute that most DTL elements have in common. If you use the <annotation> element, it must appear as the first child of the element that it is annotating.
