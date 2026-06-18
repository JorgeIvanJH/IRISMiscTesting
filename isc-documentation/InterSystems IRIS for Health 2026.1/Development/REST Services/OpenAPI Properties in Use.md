# OpenAPI Properties in Use

This page lists the properties of the OpenAPI 2.0 specification that the API management tools use when generating the REST service classes. Properties not listed here are ignored. There are several extension properties; these have names that start with `x-ISC`.

## Swagger

*   `basePath`
    
*   `consumes`
    
*   `host`
    
*   `produces`
    
*   `definitions`: Note that the API management tools do not use any properties of the Schema object when generating code.
    
*   `parameters`: For details, see Parameter Object.
    
*   `paths`: For details, see Path Item Object.
    
*   `info`: For details, see Info Object.
    
*   `swagger`: Must be `"2.0"`.
    

For details on these properties, see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#swagger-object.

## Info Object

*   `title`
    
*   `description`
    
*   `x-ISC_RequiredResource`: A comma-separated list of defined resource groups, consisting of resources and their access modes (`resource`:`mode`), that are required for access to any endpoint of the REST service. A resource group can take two forms:
    
    *   Standard Form: A resource and its access mode (resource:mode). For example, `"resource1:read"`.
        
    *   Options Form: Two or more standard form resource groups separated by a forward slash ( / ) character. This indicates that at least one of the standard form resource groups is required, but not both. For example, `"resource1:read/resource2:read"` indicates that either `"resource1:read"` or `"resource2:read"` is needed to access the REST service.
        
*   `x-ISC_ImplParent`: The name of the super class, which is a subclass of %REST.Impl, of the generated `.impl` class.
    
*   `x-ISC_DispatchParent`: The name of the super class, which is a subclass of %CSP.REST, of the generated `.disp` class.
    
*   `version`
    

For details on the standard properties, see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#info-object.

## Path Item Object

*   `$ref`
    
*   `get`, `put`, and so on (all methods listed in OpenAPI 2.0 specification are supported)
    
    Note that for the `options` method, InterSystems does not generate a stub method for you to implement. Instead, the class %CSP.REST automatically performs all `options` processing.
    
*   `parameters`: For details, see Parameter Object.
    

For details on these properties, see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#pathItemObject.

## Operation Object

*   `operationId`
    
*   `summary`
    
*   `description`
    
*   `consumes`
    
*   `produces`
    
*   `parameters`: For details, see Parameter Object.
    
*   `x-ISC_CORS`: A flag to indicate that CORS requests for this endpoint/method combination should be supported.
    
*   `x-ISC_RequiredResource`: A comma-separated list of defined resource groups, consisting of resources and their access modes (`resource`:`mode`), that are required for access to the specific operation of the REST service. Identical in syntax to the `x-ISC_RequiredResource` as explained in Info Object.
    
*   `x-ISC_ServiceMethod`: Name of the class method called on the back end to service this operation; default is `operationId`, which is normally suitable.
    
*   `responses`: Note that within the response object, `status` may be HTTP status code or `"default"`.
    

For details on the standard properties, see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#operationObject.

## Parameter Object

*   `name`
    
*   `in`
    
*   `description`
    
*   `required`
    
*   `$ref`
    
*   `type` (cannot be `"formData"`; other types are permitted)
    
*   `format`
    
*   `allowEmptyValue`
    
*   `maxLength`
    
*   `minLength`
    
*   `pattern`
    
*   `maximum`
    
*   `minimum`
    
*   `exclusiveMaximum`
    
*   `exclusiveMinimum`
    
*   `multipleOf`
    
*   `collectionFormat`
    
*   `minItems`
    
*   `maxItems`
    
*   `uniqueItems`
    
*   `items`: For details, see Items Object.
    

For details on these properties, see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#parameter-object.

## Items Object

*   `type`
    
*   `format`
    
*   `allowEmptyValue`
    
*   `maxLength`
    
*   `minLength`
    
*   `pattern`
    
*   `maximum`
    
*   `minimum`
    
*   `exclusiveMaximum`
    
*   `exclusiveMinimum`
    
*   `multipleOf`
    
*   `collectionFormat`
    
*   `minItems`
    
*   `maxItems`
    
*   `uniqueItems`
    

For details on these properties, see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#items-object.
