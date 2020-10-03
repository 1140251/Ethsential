import {
  TextDocument,
  Range,
  DiagnosticCollection,
  Diagnostic,
  DiagnosticSeverity,
  Uri,
  languages,
} from 'vscode';

import { ToolCommandIssue, ToolCommandOutput } from './toolResults';

export class DiagnosticProvider {
  private fileDiagnosticMap: Map<Uri, Diagnostic[]>;
  private diagnosticCollection: DiagnosticCollection;
  numberOfProblems = 0;

  constructor(collectionName: string) {
    this.fileDiagnosticMap = new Map<Uri, Diagnostic[]>();
    this.diagnosticCollection = languages.createDiagnosticCollection(
      collectionName
    );
  }

  public refreshDiagnostics(
    document: TextDocument,
    outputResults: ToolCommandOutput[]
  ) {
    this.clearDiagnostic(this.diagnosticCollection);
    if (outputResults.length > 0) {
      for (let i = 0; i < outputResults.length; i++) {
        if (outputResults[i].error || !outputResults[i].success) {
          continue;
        }
        this.gatherDiagnostics(outputResults[i].issues, document);
      }
      for (let [fileURI, diagnosticArray] of this.fileDiagnosticMap) {
        this.diagnosticCollection.set(fileURI, diagnosticArray);
      }
    }
    this.numberOfProblems = this.diagnosticCollection.get(
      Uri.file(document.uri.fsPath)
    ).length;
  }

  private gatherDiagnostics(
    issues: ToolCommandIssue[],
    document: TextDocument
  ) {
    if (issues.length > 0) {
      for (let j = 0; j < issues.length; j++) {
        let textRange = this.getTextRange(document, issues[j].lines);

        let severity: DiagnosticSeverity = this.getDiagnosticSeverity(
          issues[j].severity
        );
        let diagnosticResult: Diagnostic = this.createDiagnosticResult(
          textRange,
          issues[j],
          severity
        );

        let diagnosticArray = this.fileDiagnosticMap.get(document.uri);
        if (!diagnosticArray) {
          diagnosticArray = [];
          this.fileDiagnosticMap.set(document.uri, diagnosticArray);
        }
        diagnosticArray.push(diagnosticResult);
      }
    }
  }

  private createDiagnosticResult(
    textRange: Range,
    issue: ToolCommandIssue,
    severity: DiagnosticSeverity
  ) {
    let diagnosticResult: Diagnostic = new Diagnostic(
      textRange,
      issue.description ? issue.description.replace(/^\s+|\s+$/g, '') : '',
      severity
    );
    diagnosticResult.code = '';
    diagnosticResult.relatedInformation = [];
    diagnosticResult.source = '';
    return diagnosticResult;
  }

  private getTextRange(document: TextDocument, lines: Number[]) {
    let textRange: Range;
    if (lines.length > 0) {
      let firstLine = document.lineAt(lines[0].valueOf() - 1);
      let lastElement: Number = lines.pop();
      let lastLine = document.lineAt(lastElement.valueOf() - 1);
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
  }
}
