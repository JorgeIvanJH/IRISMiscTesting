# Configuring the DTL Explainer

Each DTL has a description field meant to help other users understand what the DTL does. You can configure your system to include a `Generate` button that launches an AI tool (the DTL Explainer), which examines the DTL logic and generates a detailed description. The user can include this generated text in the description field, along with manually entered text if wanted, and the resulting text is fully editable.

## On-prem Systems

To configure your system to include the DTL Explainer:

1.  Obtain a key for OpenAI.
    
2.  In an ObjectScript shell, enter the following commands:
    
    ```
    set sc = ##class(Security.Resources).Create("DTLExplainResource")
    set sc = ##class(%Wallet.Collection).Create("%DTLExplain", { "Resource": "DTLExplainResource" })
    set sc = ##class(%Wallet.KeyValue).Create("%DTLExplain.Key", { "Secret": {"token": "YourOpenAIKeyHere" }, "Usage": ["HTTP"] })
    ```
    
    After these changes, the `Generate` button will be visible in the DTL Editor, above the `Description` field for the DTL.
    

## Cloud-based Systems

If you want your system to include the DTL Explainer, create an iService ticket requesting this.

## See Also

*   Using the DTL Explainer
