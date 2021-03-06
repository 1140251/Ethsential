// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import {
  ExtensionContext,
  commands,
  TextEditor,
  window,
  workspace,
  languages,
  ProgressOptions,
  ProgressLocation,
} from 'vscode';
import * as path from 'path';
import * as net from 'net';

import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
} from 'vscode-languageclient';
import { TextDocumentIdentifier, RequestType } from 'vscode-languageserver';

import * as Docker from 'dockerode';
import { ToolCommandOutput } from './toolResults';
import { DiagnosticProvider } from './diagnosticProvider';

export let diagnosticsProvider: DiagnosticProvider;
export let analysisRunning: boolean = false;
export let installRunning: boolean = false;

let client: LanguageClient;

// Options to control the language client
const clientOptions: LanguageClientOptions = {
  documentSelector: ['solidity', 'vyper'],
};

interface ActiveAnalysisParams {
  textDocument: TextDocumentIdentifier;
  lang: string;
  tools: string[];
}
interface ActiveInstallParams {
  tools: string[];
}

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: ExtensionContext) {
  async function analyse(editor: TextEditor) {
    let serverAvailable = await checkServer();
    if (!serverAvailable) {
      window.showInformationMessage(
        `Docker is not available. Please start Docker`
      );
      return;
    }

    let pathExtension = path.extname(editor.document.fileName);
    if (!(pathExtension === '.sol' || pathExtension === '.py')) {
      window.showWarningMessage('Open a Solidity or Vyper file to analyse');
      return;
    }
    const uri = editor.document.uri.toString();
    try {
      let tools: string[] = getActiveTools();

      if (!analysisRunning) {
        analysisRunning = true;
        let progressOptions: ProgressOptions = {
          title: 'EthSential: Please wait while analysis is performed...',
          location: ProgressLocation.Notification,
          cancellable: false,
        };
        window
          .withProgress(progressOptions, async (progress, token) => {
            let result: ToolCommandOutput[] = await client.sendRequest(
              new RequestType<
                ActiveAnalysisParams,
                ToolCommandOutput[],
                void,
                void
              >('analyse'),
              {
                textDocument: { uri },
                lang: editor.document.languageId,
                tools,
              }
            );
            diagnosticsProvider.refreshDiagnostics(editor.document, result);
            analysisRunning = false;
          })
          .then(
            () => {
              window.showInformationMessage(
                `Analysis finished, found ${JSON.stringify(
                  diagnosticsProvider.numberOfProblems
                )} problems`
              );
            },
            (reason) => {
              analysisRunning = false;
              window.showErrorMessage('Failed to analyse file \n' + reason);
            }
          );
      }
    } catch (error) {
      window.showErrorMessage('Failed to analyse file');
    }
  }

  function getActiveTools() {
    const ethsential = workspace.getConfiguration('ethsential');
    const mythrilEnabled = ethsential.get<boolean>('enableMythril');
    const securifyEnabled = ethsential.get<boolean>('enableSecurify');
    const slitherEnabled = ethsential.get<boolean>('enableSlither');

    let tools: string[] = [];
    if (mythrilEnabled) {
      tools.push('mythril');
    }
    if (securifyEnabled) {
      tools.push('securify');
    }
    if (slitherEnabled) {
      tools.push('slither');
    }
    return tools;
  }

  async function install() {
    let serverAvailable = await checkServer();
    if (!serverAvailable) {
      window.showInformationMessage(
        `Docker is not available. Please start Docker`
      );
      return;
    }

    if (!installRunning) {
      installRunning = true;
      let progressOptions: ProgressOptions = {
        title: 'EthSential: Please wait while installation is performed...',
        location: ProgressLocation.Notification,
        cancellable: false,
      };

      window
        .withProgress(progressOptions, async (progress, token) => {
          let tools: string[] = getActiveTools();

          let result: String = await client.sendRequest(
            new RequestType<ActiveInstallParams, String, void, void>('install'),
            {
              tools,
            }
          );

          if (result == '200') {
            window.showInformationMessage(`Installation completed`);
          } else {
            window.showErrorMessage(
              'An error occurred during installation.\n' + result
            );
          }
          installRunning = false;
        })
        .then(
          () => {},
          () => {
            installRunning = false;
          }
        );
    }
  }

  if (isStartedInDebugMode()) {
    client = createLangServerTCP(2087);
  } else {
    client = createLangServer();
  }

  diagnosticsProvider = new DiagnosticProvider('collectionName');
  context.subscriptions.push(
    client.start(),
    commands.registerTextEditorCommand('ethsential.analyse', analyse),
    commands.registerCommand('ethsential.install', install)
  );
}

// this method is called when your extension is deactivated
export function deactivate() {}

function createLangServer(): LanguageClient {
  const cwd = path.join(__dirname, '../');

  const serverOptions: ServerOptions = {
    command: 'ethsent',
    options: { cwd },
  };
  return new LanguageClient(`ethsent`, serverOptions, clientOptions);
}

function createLangServerTCP(port: number): LanguageClient {
  const serverOptions: ServerOptions = () => {
    return new Promise((resolve, reject) => {
      const clientSocket = new net.Socket();
      clientSocket.connect(port, '127.0.0.1', () => {
        resolve({
          reader: clientSocket,
          writer: clientSocket,
        });
      });
    });
  };

  return new LanguageClient(`ethsential-client`, serverOptions, clientOptions);
}

async function checkServer(): Promise<Boolean> {
  let docker = new Docker();
  let dockerPingResponse = await docker.ping();
  return dockerPingResponse !== 'OK';
}

function isStartedInDebugMode(): boolean {
  return process.env.VSCODE_DEBUG_MODE === 'true';
}
