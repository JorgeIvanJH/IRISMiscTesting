/// Generic DTL test runner used by the iris-dtl-validate skill.
/// Parameters are passed in at call time so this class is reusable across DTLs.
Class Test.Runner [ Abstract ]
{

/// Run pDTLClass against the HL7 message at pInFile and write the resulting
/// HL7 message to pOutFile. pSourceDocType (e.g. "2.3.1:ADT_A06") is assigned
/// to the imported source message ONLY if it is non-empty AND the imported
/// message did not already have a DocType resolved from its MSH segment.
/// Prints RESULT markers so the shell/Python wrapper can detect outcome.
ClassMethod Run(pDTLClass As %String, pSourceDocType As %String, pInFile As %String, pOutFile As %String) As %Status
{
	set sc = 1
	try {
		set source = ##class(EnsLib.HL7.Message).ImportFromFile(pInFile,,.sc)
		if $system.Status.IsError(sc) throw ##class(%Exception.StatusException).CreateFromStatus(sc)
		if (source.DocType="")&&(pSourceDocType'="") set source.DocType=pSourceDocType
		write "Source: DocType=",source.DocType,", segments=",source.SegCount,!

		set sc = $classmethod(pDTLClass,"Transform",source,.target)
		if $system.Status.IsError(sc) throw ##class(%Exception.StatusException).CreateFromStatus(sc)
		write "Target: DocType=",target.DocType,", segments=",target.SegCount,!

		// OutputToFile appends; ensure a clean target file each run.
		if ##class(%File).Exists(pOutFile) do ##class(%File).Delete(pOutFile)
		set sc = target.OutputToFile(pOutFile)
		if $system.Status.IsError(sc) throw ##class(%Exception.StatusException).CreateFromStatus(sc)

		write "Wrote ",pOutFile,!
		write "RESULT=OK",!
	} catch ex {
		set sc = ex.AsStatus()
		write "RESULT=ERROR",!
		write "  ",$system.Status.GetErrorText(sc),!
	}
	quit sc
}

}
