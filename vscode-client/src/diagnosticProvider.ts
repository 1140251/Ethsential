import {
  TextDocument,
  Range,
  DiagnosticCollection,
  Diagnostic,
  DiagnosticSeverity,
  Uri,
  languages,
} from 'vscode';

import { ToolCommandIssues, ToolCommandOutput } from './toolResults';

export class DiagnosticProvider {
  private fileDiagnosticMap: Map<Uri, Diagnostic[]>;
  private fileResultMap: Map<string, ToolCommandIssues[]>;
  private diagnosticCollection: DiagnosticCollection;
  numberOfProblems = 0;

  constructor(collectionName: string) {
    this.fileDiagnosticMap = new Map<Uri, Diagnostic[]>();
    this.fileResultMap = new Map<string, ToolCommandIssues[]>();
    this.diagnosticCollection = languages.createDiagnosticCollection(
      collectionName
    );
  }

  public refreshDiagnostics(
    document: TextDocument,
    outputResults: ToolCommandOutput[]
  ) {
    // Clear the diagnostic.
    this.clearDiagnostic(this.diagnosticCollection);

    if (outputResults.length > 0) {
      for (let i = 0; i < outputResults.length; i++) {
        if (outputResults[i].error || !outputResults[i].success) {
          continue;
        }

        if (outputResults[i].issues.length > 0) {
          for (let j = 0; j < outputResults[i].issues.length; j++) {
            let textRange = this.getTextRange(
              document,
              outputResults[i].issues[j].lines
            );

            let severity: DiagnosticSeverity = this.getDiagnosticSeverity(
              outputResults[i].issues[j].severity
            );
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
        this.diagnosticCollection.set(fileURI, diagnosticArray);
      }
    }

    this.numberOfProblems = this.diagnosticCollection.get(
      Uri.file(document.uri.fsPath)
    ).length;
  }

  private getTextRange(document: TextDocument, lines: Number[]) {
    let textRange: Range;
    if (lines.length > 0) {
      let firstLine = document.lineAt(lines[0].valueOf());
      let lastElement: Number = lines.pop();
      let lastLine = document.lineAt(lastElement.valueOf());
      textRange = new Range(firstLine.range.start, lastLine.range.end);
    }
    return textRange;
  }

  private getDiagnosticSeverity(severity: string) {
    let dSeverity: DiagnosticSeverity = DiagnosticSeverity.Information;
    switch (severity.toLowerCase()) {
      case 'critical':
      case 'high':
        dSeverity = DiagnosticSeverity.Error;
        break;
      case 'medium':
      case 'low':
        dSeverity = DiagnosticSeverity.Warning;
        break;
      case 'optimization':
        dSeverity = DiagnosticSeverity.Hint;
      default:
        dSeverity = DiagnosticSeverity.Information;
        break;
    }
    return dSeverity;
  }

  private clearDiagnostic(diagnosticCollection: DiagnosticCollection) {
    diagnosticCollection.clear();
    this.numberOfProblems = 0;
    this.fileDiagnosticMap.clear();
    this.fileResultMap.clear();
  }
}
