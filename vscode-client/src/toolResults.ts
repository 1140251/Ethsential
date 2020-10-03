export interface ToolCommandOutput {
  success: boolean;
  error: string | null | undefined;
  issues: ToolCommandIssue[] | null | undefined;
  duration: Number | undefined;
}

export interface ToolCommandIssue {
  severity: string;
  pattern: string;
  description: string;
  lines: Number[];
  function: string;
  contract: string;
}
