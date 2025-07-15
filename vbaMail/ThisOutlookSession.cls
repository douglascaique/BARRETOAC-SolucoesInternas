VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ThisOutlookSession"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Sub SaveAttachmentsIgnoreImages(Item As MailItem)
    Dim olApp As Outlook.Application
    Dim olNamespace As Outlook.NameSpace
    Dim olFolder As Outlook.Folder
    Dim olItem As Object
    Dim olAttachment As Attachment
    Dim savePath As String
    Dim fileExtension As String

    ' Caminho para salvar os arquivos
    savePath = "C:\Users\geral\Downloads\testee\"

    ' Verificar se o caminho termina com barra invertida
    If Right(savePath, 1) <> "\" Then
        savePath = savePath & "\"
    End If

    ' Configurar o Outlook e iterar pelos emails
    Set olApp = Outlook.Application
    Set olNamespace = olApp.GetNamespace("MAPI")
    Set olFolder = olNamespace.Folders("apoiofiscal2@barretoac.com.br").Folders("Caixa de Entrada").Folders("TESTE")

    For Each olItem In olFolder.Items
        If olItem.Attachments.Count > 0 Then
            For Each olAttachment In olItem.Attachments
                ' Obter a extensão do arquivo
                fileExtension = LCase(Right(olAttachment.FileName, Len(olAttachment.FileName) - InStrRev(olAttachment.FileName, ".")))

                ' Ignorar arquivos com extensão de imagem
                If fileExtension <> "jpg" And fileExtension <> "jpeg" And fileExtension <> "png" And fileExtension <> "gif" And fileExtension <> "bmp" Then
                    olAttachment.SaveAsFile savePath & olAttachment.FileName
                End If
            Next olAttachment
        End If
    Next olItem

    MsgBox "Anexos salvos com sucesso em " & savePath
End Sub
