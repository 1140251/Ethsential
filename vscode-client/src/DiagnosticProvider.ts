import {
  CodeActionProvider,
  TextDocument,
  Range,
  Selection,
  CodeActionContext,
  CancellationToken,
  ProviderResult,
  Command,
  CodeAction,
  DiagnosticCollection,
  Diagnostic,
  DiagnosticSeverity,
  ExtensionContext,
  TextEditor,
  Uri,
} from 'vscode';

import { ToolCommandIssues, ToolCommandOutput } from './ToolResults';

export class DiagnosticProvider {
  private fileDiagnosticMap: Map<Uri, Diagnostic[]>;
  private fileResultMap: Map<string, ToolCommandIssues[]>;

  constructor() {
    // Set the diagnostic collection for this provider.

    // Initialize our file->result map to pair workspace results with diagnostics.
    this.fileDiagnosticMap = new Map<Uri, Diagnostic[]>();
    this.fileResultMap = new Map<string, ToolCommandIssues[]>();
  }

  public refreshDiagnostics(
    document: TextDocument,
    outputResults: ToolCommandOutput[],
    diagnosticCollection: DiagnosticCollection
  ): number {
    try {
      // Clear the diagnostic collection.
      diagnosticCollection.clear();

      // Clear our result and diagnostic maps
      this.fileDiagnosticMap.clear();
      this.fileResultMap.clear();
      if (outputResults.length > 0) {
        for (let i = 0; i < outputResults.length; i++) {
          if (outputResults[i].error || !outputResults[i].success) {
            continue;
          }

          if (outputResults[i].success && outputResults[i].issues.length > 0) {
            for (let j = 0; j < outputResults[i].issues.length; j++) {
              let firstLine = document.lineAt(
                outputResults[i].issues[j].lines[0].valueOf()
              );
              let lastElement: Number = outputResults[i].issues[j].lines.pop();
              let lastLine = document.lineAt(lastElement.valueOf());
              let textRange = new Range(
                firstLine.range.start,
                lastLine.range.end
              );

              let severity: DiagnosticSeverity = DiagnosticSeverity.Information;
              switch (outputResults[i].issues[j].severity.toLowerCase()) {
                case 'critical':
                case 'high':
                  severity = DiagnosticSeverity.Error;
                  break;
                case 'medium':
                case 'low':
                  severity = DiagnosticSeverity.Warning;
                  break;
                default:
                  severity = DiagnosticSeverity.Information;
                  break;
              }
              let diagnosticResult: Diagnostic = new Diagnostic(
                textRange,
                outputResults[i].issues[j].description
                  ? outputResults[i].issues[j].description.replace(
                      /^\s+|\s+$/g,
                      ''
                    )
                  : '',
                severity
              );
              diagnosticResult.code = '';
              diagnosticResult.relatedInformation = [];
              diagnosticResult.source = '';

              let diagnosticArray = this.fileDiagnosticMap.get(document.uri);
              let resultArray = this.fileResultMap.get(document.uri.fsPath);
              if (!diagnosticArray || !resultArray) {
                diagnosticArray = [];
                resultArray = [];
                this.fileDiagnosticMap.set(document.uri, diagnosticArray);
                this.fileResultMap.set(document.uri.fsPath, resultArray);
              }
              diagnosticArray.push(diagnosticResult);
              resultArray.push(outputResults[i].issues[j]);
            }
          }
        }

        for (let [fileURI, diagnosticArray] of this.fileDiagnosticMap) {
          diagnosticCollection.set(fileURI, diagnosticArray);
        }
      }

      return diagnosticCollection.get(Uri.file(document.uri.fsPath)).length;
    } catch (error) {
      return 0;
    }
  }
}
